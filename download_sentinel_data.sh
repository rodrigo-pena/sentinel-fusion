s2_folder='data/Sentinel-2'
s3_folder='data/Sentinel-3'
aoi='data/geometry/greater-geneva-rectangle.geojson'
#start_date=20200805
#end_date=20200806
start_date=20200818
end_date=20200823
username=$(awk '/scihub.copernicus.eu/{getline; print $2}' ~/.netrc)
password=$(awk '/scihub.copernicus.eu/{getline; getline; print $2}' ~/.netrc)
cloud_cover_percentage=30

python download_sentinel_data.py --aoi_geojson ${aoi} --start_date ${start_date} --end_date ${end_date} --platform Sentinel-2 --username ${username} --password ${password} --download_path ${s2_folder} --download_images True --cloud_cover_percentage ${cloud_cover_percentage}

python download_sentinel_data.py --aoi_geojson ${aoi} --start_date ${start_date} --end_date ${end_date} --platform Sentinel-3 --username ${username} --password ${password} --download_path ${s3_folder} --download_images True --cloud_cover_percentage ${cloud_cover_percentage}