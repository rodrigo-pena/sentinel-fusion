s2_folder='data/Sentinel-2'
s3_folder='data/Sentinel-3'
aoi='data/geometry/greater-geneva-rectangle.geojson'
start_date=20200805
end_date=20200806
username=$(awk '/scihub.copernicus.eu/{getline; print $2}' ~/.netrc)
password=$(awk '/scihub.copernicus.eu/{getline; getline; print $2}' ~/.netrc)
cloud_cover_percentage=30

python sentinel_data_download.py --aoi_geojson ${aoi} --start_date ${start_date} --end_date ${end_date} --platform Sentinel-2 --username ${username} --password ${password} --download_path ${s2_folder} --download_images True --cloud_cover_percentage ${cloud_cover_percentage}

python sentinel_data_download.py --aoi_geojson ${aoi} --start_date ${start_date} --end_date ${end_date} --platform Sentinel-3 --username ${username} --password ${password} --download_path ${s3_folder} --download_images True --cloud_cover_percentage ${cloud_cover_percentage}