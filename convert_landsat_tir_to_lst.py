"""
Conversion of Lansat 8 TIR to LST, based on [Avdan & Jovanovska 2016]
(http://dx.doi.org/10.1155/2016/1480307). See also https://tinyurl.com/y5ntexyx
"""
import os
import click
import tempfile

import numpy as np
import gdal_utils as gu
import snappy_utils as su

from glob import glob
from osgeo import gdal
from snappy import ProductIO


def get_conversion_params(metadata_file, band_number=10):
    """Extract conversion parameters from the Landsat Level-1 metadata file.

    Parameters
    ----------
    metadata_file : string
        Path to the MTL file in the Landsat Level-1 product.
    band_number : int, optional
        Number of the Landsat Level-1 TIR band of interest (should be either 10
        or 11), by default 10

    Returns
    -------
    dict
        Dictionary of parameters with the follwing key-value pairs:
            radiance_mult_band: float
                Band-specific multiplicative rescaling factor for radiance
                conversion
            radiance_add_band : float
                Band-specific additive rescaling factor for radiance conversion
            k1 : float
                Band-specific thermal constant (k1) for temperature conversion
            k2 : float
                Band-specific thermal constant (k2) for temperature conversion

    References
    ----------
    https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product
    """

    params = dict()

    with open(metadata_file) as metadata:
        for line in metadata:

            if line.find('RADIANCE_MULT_BAND_'+'{}'.format(band_number)) != -1:
                equals_sign_pos = line.find('=')
                params['radiance_mult_band'] = float(line[equals_sign_pos+2:])

            if line.find('RADIANCE_ADD_BAND_'+'{}'.format(band_number)) != -1:
                equals_sign_pos = line.find('=')
                params['radiance_add_band'] = float(line[equals_sign_pos+2:])

            if line.find('K1_CONSTANT_BAND_'+'{}'.format(band_number)) != -1:
                equals_sign_pos = line.find('=')
                params['k1'] = float(line[equals_sign_pos+2:])

            if line.find('K2_CONSTANT_BAND_'+'{}'.format(band_number)) != -1:
                equals_sign_pos = line.find('=')
                params['k2'] = float(line[equals_sign_pos+2:])

    return params


def dn_to_radiance(raster, radiance_mult_band, radiance_add_band):
    """Convert raster from Digital Numbers (DN) to Top-Of-Atmosphere (TOA)
    radiance.

    Parameters
    ----------
    raster : array
        Matrix of DN values for the Landsat Level-1 TIR band 10 or 11.
    radiance_mult_band : float
        Band-specific multiplicative rescaling factor from the metadata of
        Landsat Level-1 TIR band 10 or 11.
    radiance_add_band : float
        Band-specific additive rescaling factor from the metadata of Landsat
        Level-1 TIR band 10 or 11.

    Returns
    -------
    array
        Matrix of TOA spectral radiance values for the Landsat Level-1 TIR band
        10 or 11.

    References
    ----------
    https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product
    """
    return (raster * radiance_mult_band) + radiance_add_band


def radiance_to_bt(raster, k1, k2):
    """Convert raster from Top-Of-Atmosphere (TOA) spectral radiance to TOA
    brightness temperature, in Kelvin.

    Parameters
    ----------
    raster : array
        Matrix of TOA spectral radiance values for the Landsat Level-1 TIR band
        10 or 11.
    k1 : float
        Band-specific thermal conversion constant from the metadata of
        Landsat Level-1 TIR band 10 or 11.
    k2 : float
        Band-specific thermal conversion constant from the metadata of
        Landsat Level-1 TIR band 10 or 11.

    Returns
    -------
    array
        Matrix of TOA brightness temperature values (in Kelvin) for the
        Landsat Level-1 TIR band 10 or 11.

    References
    ----------
    https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product
    """
    return k2 / np.log((k1 / raster) + 1)


def ndvi(landsat_product_path, nir_band=5, red_band=4):
    """Calculates the Normal Difference Vegetation Index (NDVI) based on the
    near-infrared and red bands of Landsat

    Parameters
    ----------
    landsat_product_path : string
        Path to the the Landsat folder containing the GeoTiff images of the
        bands
    nir_band : int, optional
        Number of the near-infrared band, by default 5
    red_band : int, optional
        Number of the red band, by default 4

    Returns
    -------
    array
        The NDVI raster
    """
    # Find files for NIR and RED bands
    nir_files = glob(os.path.join(landsat_product_path,
                                  '*_B{}*'.format(nir_band)))
    red_files = glob(os.path.join(landsat_product_path,
                                  '*_B{}*'.format(red_band)))

    # If more than one matching file for each band, open the first match by
    # default
    try:
        nir_file = nir_files[0]
    except IndexError:
        print("Found zero files corresponding to band {}".format(nir_band))
    try:
        red_file = red_files[0]
    except IndexError:
        print("Found zero files corresponding to band {}".format(red_band))

    nir_data = gdal.Open(nir_file)
    nir_raster = nir_data.GetRasterBand(1).ReadAsArray().astype(float)
    red_data = gdal.Open(red_file)
    red_raster = red_data.GetRasterBand(1).ReadAsArray().astype(float)

    # Calculate NDVI
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi_raster = (nir_raster - red_raster) / (nir_raster + red_raster)
    ndvi_raster[np.isinf(ndvi_raster)] = np.nan  # Correct for division by zero

    # Close the datasets
    nir_data = None
    red_data = None

    return ndvi_raster


def proportion_of_vegetation(ndvi_raster, ndvi_v=0.5, ndvi_s=0.2):
    """Estimates Proportion of Vegetation (Pv) from the Normal Difference
    Vegetation Index (NDVI)

    Parameters
    ----------
    ndvi_raster : array
        The NDVI raster
    ndvi_v : float, optional
        NDVI value for vegetation, by default 0.5
    ndvi_s : float, optional
        NDVI value for soil, by default 0.2

    Returns
    -------
    array
        The Pv raster
    """
    return ((ndvi_raster - ndvi_s) / (ndvi_v - ndvi_s)) ** 2


def land_surface_emissivity(landsat_product_path,
                            emissivity_water=0.991,
                            emissivity_soil=0.966,
                            emissivity_vegetation=0.973,
                            surface_roughness=0.005,
                            nir_band=5,
                            red_band=4,
                            ndvi_v=0.5,
                            ndvi_s=0.2):
    """Estimate Land Surface Emissivity (LSE)

    Parameters
    ----------
    landsat_product_path : string
        Path to the the Landsat folder containing the GeoTiff images of the
        bands
    emissivity_water : float, optional
        Water emissivity, by default 0.991
    emissivity_soil : float, optional
        Soil emissivity, by default 0.966
    emissivity_vegetation : float, optional
        Vegetation emissivity, by default 0.973
    surface_roughness : float, optional
        Surface roughness constant, by default 0.005
    nir_band : int, optional
        Number of the near-infrared band, by default 5
    red_band : int, optional
        Number of the red band, by default 4
    ndvi_v : float, optional
        NDVI value for vegetation, by default 0.5
    ndvi_s : float, optional
        NDVI value for soil, by default 0.2

    Returns
    -------
    array
        The LSE raster
    """

    ndvi_raster = ndvi(landsat_product_path, nir_band, red_band)
    Pv = proportion_of_vegetation(ndvi_raster, ndvi_v, ndvi_s)

    # 1. Mixed surfaces
    emissivity = emissivity_vegetation * Pv + emissivity_soil * (1 - Pv) + \
        surface_roughness

    # 2. Water
    emissivity[ndvi_raster < 0] = emissivity_water

    # 3. Pure soil
    emissivity[(ndvi_raster >= 0) & (ndvi_raster < ndvi_s)] = emissivity_soil

    # 4. Pure vegetation
    emissivity[ndvi_raster > ndvi_v] = emissivity_vegetation

    return emissivity


def bt_to_lst(raster, lse, band_number=10):
    """Convert at-sensor Brightness Temperature (BT) to Land Surface
    Temperature (LST), in Kelvin.

    Parameters
    ----------
    raster : array
        Matrix of BT values for the Landsat Level-1 TIR band 10 or 11
    lse : array
        Matrix of land surface emissivities
    band_number : int, optional
        Number of the Landsat Level-1 TIR band of interest (should be either 10
        or 11), by default 10

    Returns
    -------
    array
        The LST raster

    Raises
    ------
    ValueError
        If `band_number` is neither `10` nor `11`
    """
    # Set average sensing wavelength. Taken from https://tinyurl.com/y6gdpgk8
    if band_number == 10:
        wavelength = ((10.6 + 11.19) / 2) * 1e-6
    elif band_number == 11:
        wavelength = ((11.5 + 12.51) / 2) * 1e-6
    else:
        raise ValueError("Variable 'band_number' should take value 10 or 11.")

    # Set (Planck's constant) * (speed of light) * (Boltzmann's constant)
    rho = 1.438e-2

    return raster / (1 + (wavelength * raster * np.log(lse) / rho))


@click.command()
@click.option('--landsat_product_path', required=True,
              type=click.Path(dir_okay=True, exists=True))
@click.option('--band_number', required=True,
              type=click.IntRange(10, 11))
@click.option('--lst_output', required=True,
              type=click.Path(dir_okay=False, exists=False))
def main(landsat_product_path, band_number, lst_output):

    # Find files for the specified TIR band
    tir_files = glob(os.path.join(landsat_product_path,
                                  '*_B{}*'.format(band_number)))
    try:
        # If more than one matching file, open the first match by default
        tir_file = tir_files[0]
    except IndexError:
        print("Found zero files corresponding to band {}".format(band))
    tir_data = gdal.Open(tir_file)
    tir_raster = tir_data.GetRasterBand(1).ReadAsArray().astype(float)

    # Get conversion parameters from the metadata
    metadata_files = glob(os.path.join(landsat_product_path, '*_MTL*'))
    try:
        # If more than one matching file, open the first match by default
        metadata_file = metadata_files[0]
    except IndexError:
        print("Found zero metadata (MTL) files")
    params = get_conversion_params(metadata_file, band_number)

    print('INFO: Converting DN to TOA spectral radiance...')
    radiance = dn_to_radiance(tir_raster,
                              params['radiance_mult_band'],
                              params['radiance_add_band'])

    print('INFO: Converting TOA spectral radiance to ' +
          'at-sensor brightness temperature...')
    bt = radiance_to_bt(radiance, params['k1'], params['k2'])

    print('INFO: Estimating land surface emissivity...')
    lse = land_surface_emissivity(landsat_product_path)

    print('INFO: Converting at-sensor brightness temperature to ' +
          'land surface temperature...')
    lst = bt_to_lst(bt, lse, band_number)

    # Write estimated LST into new GeoTiff
    print('INFO: Saving GeoTiff output...')
    driver = gdal.GetDriverByName("GTiff")
    driver.Register()
    # Ensure that output is saved in GeoTiff format
    lst_output = os.path.splitext(lst_output)[0] + '.TIF'
    lst_data = driver.CreateCopy(lst_output, tir_data, strict=0)
    lst_data.GetRasterBand(1).WriteArray(lst)
    lst_data.GetRasterBand(1).FlushCache()

    # Clean up
    tir_data = None
    lst_data = None

    # # Write the LST as a BEAM-DIMAP product as well
    print('INFO: Saving BEAM_DIMAP output...')
    product = ProductIO.readProduct(lst_output)
    band = {
        "band_name": "LST",
        "description": "LST estimated from Landsat TIR",
        "unit": "K",
        "band_data": lst
    }
    geo_coding = product.getSceneGeoCoding()
    # Ensure that output is saved in BEAM-DIMAP format
    lst_output = os.path.splitext(lst_output)[0] + '.dim'
    su.write_snappy_product(lst_output, [band], "Landsat_LST", geo_coding)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:" + str(e))
