import click
import tempfile
import numpy as np
import os
import os.path as pth

from pyDMS.pyDMS import DecisionTreeSharpener

import gdal_utils as gu
import snappy_utils as su


@click.command()
@click.option('--high_res_reflectance', required=True,
              type=click.Path(dir_okay=False, exists=True))
@click.option('--low_res_lst', required=True,
              type=click.Path(dir_okay=False, exists=True))
@click.option('--high_res_dem', required=True,
              type=click.Path(dir_okay=False, exists=True))
@click.option('--lst_quality_mask', required=True,
              type=click.Path(dir_okay=False, exists=True))
@click.option('--elevation_band', required=True)
@click.option('--lst_good_quality_flags', required=True)
@click.option('--cv_homogeneity_threshold', required=True,
              type=click.FloatRange(0, 1))
@click.option('--moving_window_size', required=True,
              type=click.IntRange(1))
@click.option('--parallel_jobs', required=True,
              type=click.IntRange(1))
@click.option('--output', required=True,
              type=click.Path(dir_okay=False, exists=False))
def main(high_res_reflectance,
         low_res_lst,
         high_res_dem,
         lst_quality_mask,
         elevation_band,
         lst_good_quality_flags,
         cv_homogeneity_threshold,
         moving_window_size,
         parallel_jobs,
         output):

    print('INFO: Preparing high-resolution data...')
    # Elevation
    temp_file = tempfile.NamedTemporaryFile(suffix=".tif", delete=False)
    temp_dem_file = temp_file.name
    temp_file.close()
    su.copy_bands_to_file(high_res_dem, temp_dem_file, [elevation_band])
    # Reflectance
    temp_file = tempfile.NamedTemporaryFile(suffix=".tif", delete=False)
    temp_refl_file = temp_file.name
    temp_file.close()
    su.copy_bands_to_file(high_res_reflectance, temp_refl_file)
    # Combine all high-resolution data into one virtual raster
    vrt_filename = pth.splitext(temp_refl_file)[0] + ".vrt"
    fp = gu.merge_raster_layers([temp_refl_file, temp_dem_file],
                                vrt_filename, separate=True)
    fp = None
    high_res_filename = vrt_filename

    print('INFO: Preparing low-resolution data...')
    # LST
    temp_file = tempfile.NamedTemporaryFile(suffix=".tif", delete=False)
    temp_lst_file = temp_file.name
    temp_file.close()
    su.copy_bands_to_file(low_res_lst, temp_lst_file, ["LST"])
    # Quality mask
    temp_file = tempfile.NamedTemporaryFile(suffix=".tif", delete=False)
    temp_mask_file = temp_file.name
    temp_file.close()
    su.copy_bands_to_file(lst_quality_mask, temp_mask_file)

    # Set disaggregator options
    flags = [int(i) for i in lst_good_quality_flags.split(",")]
    dms_options = {"highResFiles": [high_res_filename],
                   "lowResFiles": [temp_lst_file],
                   "lowResQualityFiles": [temp_mask_file],
                   "lowResGoodQualityFlags": flags,
                   "cvHomogeneityThreshold": cv_homogeneity_threshold,
                   "movingWindowSize": moving_window_size,
                   "disaggregatingTemperature":  True,
                   "baggingRegressorOpt": {"n_jobs": parallel_jobs,
                                           "n_estimators": 30,
                                           "max_samples": 0.8,
                                           "max_features": 0.8}}
    disaggregator = DecisionTreeSharpener(**dms_options)

    # Sharpen
    print("INFO: Training regressor...")
    disaggregator.trainSharpener()
    print("INFO: Sharpening...")
    downscaled_file = disaggregator.applySharpener(high_res_filename,
                                                   temp_lst_file)
    print("INFO: Residual analysis...")
    residual_image, corrected_image = disaggregator.residualAnalysis(
        downscaled_file,
        temp_lst_file,
        temp_mask_file,
        doCorrection=True
    )
    # Save the sharpened file
    band = {
        "band_name": "LST",
        "description": "Sharpened Sentinel-3 LST",
        "unit": "K",
        "band_data": corrected_image.GetRasterBand(1).ReadAsArray()
    }
    geo_coding = su.get_product_info(high_res_reflectance)[1]
    su.write_snappy_product(output, [band], "sharpenedLST", geo_coding)

    # Clean up
    try:
        os.remove(temp_dem_file)
        os.remove(temp_refl_file)
        os.remove(temp_lst_file)
        os.remove(temp_mask_file)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:" + str(e))
