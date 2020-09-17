# Sentinel products
s2_folder='data/Sentinel-2/'
s2_product='S2A_MSIL2A_20200805T104031_N0214_R008_T31TGM_20200805T121101.dim'
s3_folder='data/Sentinel-3/'
s3_product='S3A_SL_2_LST____20200805T094312_20200805T094612_20200806T151948_0179_061_193_2160_LN2_O_NT_004.dim'

# Parameters for data_mining_sharpener.py
s2_reflectance=${s2_folder}processed_reflectance.dim
s2_dem=${s2_folder}processed_elevation.dim
s3_lst=${s3_folder}processed_lst.dim
s3_geom=${s3_folder}processed_high_res_geom.dim
s3_mask=${s3_folder}processed_mask.dim
date_time_utc='2020-08-05 09:43'  # ATTENTION: change according to S3 product
elevation_band=elevation
lst_good_quality_flags=1
cv_homogeneity_threshold=0
moving_window_size=15
parallel_jobs=1
output_lst_sharp=${s3_folder}output_lst_sharp.dim

python data_mining_sharpener.py --sentinel_2_reflectance ${s2_reflectance} --sentinel_3_lst ${s3_lst} --high_res_dem ${s2_dem} --high_res_geom ${s3_geom} --lst_quality_mask ${s3_mask} --date_time_utc "${date_time_utc}" --elevation_band ${elevation_band} --lst_good_quality_flags ${lst_good_quality_flags} --cv_homogeneity_threshold ${cv_homogeneity_threshold} --moving_window_size ${moving_window_size} --parallel_jobs ${parallel_jobs} --output ${output_lst_sharp}