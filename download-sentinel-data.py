# Download data from Sentinel-2 and Sentinel-3

import argparse
import sys
import os

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from zipfile import ZipFile, BadZipfile
from datetime import datetime

DHUS_URL = 'https://scihub.copernicus.eu/dhus'
DATA_DIR = os.path.join(os.getcwd(), 'data')
DEFAULT_GEOJSON = 'greater-geneva-rectangle.geojson'


def create_folder(folder_name, root_path=os.getcwd()):
    """Create a new folder at the specified root path

    Parameters
    ----------
    folder_name : str
        The name of the new folder
    root_path : str, optional
        The path to the root folder, by default os.getcwd()

    Returns
    -------
    int
        Returns 1 if the folder was successfully created, or 0 if the folder
        already existed.
    """
    composed_path = os.path.join(root_path, folder_name)
    if not os.path.isdir(composed_path):
        os.mkdir(composed_path)  # Create folder
        return 1
    else:
        return 0  # Do nothing; folder already exists


def unzip_all(path):
    """Unzips all files within the specified folder path

    Parameters
    ----------
    path : str
        Path to the folder containing the .zip files to be unziped.
    """
    for file_name in os.listdir(path):
        if file_name.endswith(".zip"):
            folder_name = os.path.splitext(os.path.basename(file_name))[0]
            file_path = os.path.join(path, file_name)
            try:
                zip_obj = ZipFile(file_path)
                zip_obj.extractall(path=path)
                try:
                    os.remove(file_path)  # Remove leftover zip files
                except OSError as err:
                    if err.errno != errno.ENOENT:
                        raise
            except BadZipfile:
                print("Bad zip: {}".format(file_name))
    return


def download(area, date, platformname):
    """Download data based on area, date and platform name

    Parameters
    ----------
    area : (str, optional)
        Area of interest formatted as a Well-Known Text.
    date : (tuple of (str or datetime) or str, optional)
        A time interval filter based on the Sensing Start Time of the products.
    platformname : (str)
        Either 'Sentinel-2' or 'Sentinel-3'.

    Returns
    -------
    products : (dict[string, dict])
        Products returned by the query as a dictionary.
    size : (float)
        Total file size in GB.
    info : ()
        Dictionary containing the return value for each successfully
        downloaded product.
    """
    if (platformname == 'Sentinel-2'):
        producttype = 'S2MSI2A'
    elif (platformname == 'Sentinel-3'):
        producttype = 'SL_2_LST___'
    else:
        return None, None, None

    # Query SciHub for Sentinel data
    products = api.query(area=area,
                         date=date,
                         area_relation='Intersects',
                         platformname=platformname,
                         producttype=producttype)

    size = api.get_products_size(products)

    # Check if user really wants to download all this data
    proceed = None
    while (proceed != 'y') and (proceed != 'n'):
        proceed = input("Download {} GB of ".format(size) +
                        "{} data? (y/n)\n".format(platformname))

    if (proceed == 'y'):
        pass
    else:
        return None, None, None

    # Make sure downloads directory exists
    create_folder(platformname, DATA_DIR)

    # Download all products found for the Sentinel query
    directory_path = os.path.join(DATA_DIR, platformname)
    info = api.download_all(products, directory_path=directory_path)

    return products, size, info


if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download Sentinel Data.')
    parser.add_argument('-user',
                        default=None,
                        type=str,
                        action='store',
                        dest='user',
                        help="Username for the Copernicus Open Access Hub." +
                        " It defaults to the value in the DHUS_USER" +
                        " variable" +
                        " in the system's path, or to the value described in" +
                        " the .netrc file at the computer user's home" +
                        " directory.")
    parser.add_argument('-password',
                        default=None,
                        type=str,
                        action='store',
                        dest='password',
                        help="Password for the Copernicus Open Access Hub." +
                        " It defaults to the value in the DHUS_PASSWORD" +
                        " variable" +
                        " in the system's path, or to the value described in" +
                        " the .netrc file at the computer user's home" +
                        " directory.")
    parser.add_argument('-aoi',
                        default=None,
                        type=str,
                        action='store',
                        dest='aoi',
                        help="Path to area of interest in geojson format." +
                        " It defaults to 'data/switzerland.geojson'.")
    args = parser.parse_args()

    # Create Sentinel API object
    api = SentinelAPI(args.user, args.password, DHUS_URL)

    # Area of interest in Well-Known Text format
    if (args.aoi is None):
        geojson_path = os.path.join(DATA_DIR, 'geometry', DEFAULT_GEOJSON)
    else:
        geojson_path = args.aoi
    area = geojson_to_wkt(read_geojson(geojson_path))

    # Period of interest as a tuple (start, end)
    # Sentinel-2 covers the globe in 5 days; Sentinel-3 does it every day.
    # Taking at least 5 days ensures that both satellites measure the AOI
    # specified in the .geojson file.
    date = (datetime(2020, 8, 1, 0, 0, 0, 0),
            datetime(2020, 8, 7, 0, 0, 0, 0))

    s2_products, s2_size, s2_info = download(area, date, 'Sentinel-2')
    s3_products, s3_size, s3_info = download(area, date, 'Sentinel-3')

    # Unzip all the downloaded files
    unzip_all(os.path.join(DATA_DIR, 'Sentinel-2'))
    unzip_all(os.path.join(DATA_DIR, 'Sentinel-3'))
