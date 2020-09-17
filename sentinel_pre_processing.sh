# ATTENTION: Change the file pointers below according to the downloaded files you actually want to explore
s2_folder='data/Sentinel-2/'
s2_product='S2A_MSIL2A_20200805T104031_N0214_R008_T31TGM_20200805T121101.dim'

s3_folder='data/Sentinel-3/'
s3_product='S3A_SL_2_LST____20200805T094312_20200805T094612_20200806T151948_0179_061_193_2160_LN2_O_NT_004.dim'

# Parameters for the SNAP pre-processing graphs
aoi='POLYGON((5.63614201613131 46.48730740760096, 6.399441865096295 46.4671492804572, 6.374261461965352 46.05871378389698, 5.616597452606011 46.07858807515982, 5.63614201613131 46.48730740760096))'
crs=EPSG:4326
output_reflectance=${s2_folder}processed_reflectance.dim
output_elevation=${s2_folder}processed_elevation.dim
output_observation_geometry=${s3_folder}processed_observation_geometry.dim
output_mask=${s3_folder}processed_mask.dim
output_lst=${s3_folder}processed_lst.dim
max_parallel_threads=40

# Parameters for warp_to_template.py
source=${output_observation_geometry}
template=${output_reflectance}
output_high_res_geom=${s3_folder}processed_high_res_geom.dim

# Run the Sentinel-2 product through its preprocessing pipeline
# gpt snap_graphs/sentinel_2_pre_processing.xml -p snap_graphs/sentinel_2_pre_processing.properties -Pinput=${s2_folder}${s2_product} -Paoi='$aoi' -q ${max_parallel_threads}
gpt snap_graphs/sentinel_2_pre_processing.xml -Pinput=${s2_folder}${s2_product} -Paoi=${aoi} -Pcrs=${crs} -Poutput_reflectance=${output_reflectance} -Poutput_elevation=${output_elevation} -q ${max_parallel_threads}

# Run the Sentinel-3 product through its preprocessing pipeline
# gpt snap_graphs/sentinel_3_pre_processing.xml -p snap_graphs/sentinel_3_pre_processing.properties -Pinput=${s3_folder}${s3_product} -Paoi='$aoi' -q ${max_parallel_threads}
gpt snap_graphs/sentinel_3_pre_processing.xml -p snap_graphs/sentinel_3_pre_processing.properties -Pinput=${s3_folder}${s3_product} -Paoi=${aoi} -Pcrs=${crs} -Poutput_observation_geometry=${output_observation_geometry} -Poutput_mask=${output_mask} -Poutput_lst=${output_lst} -q ${max_parallel_threads}

python warp_to_template.py --source ${source} --template ${template} --output ${output_high_res_geom}