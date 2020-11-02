# ATTENTION: Change the file pointers below according to the downloaded files you actually want to explore
s2_folder='data/Sentinel-2/'
s2_product='S2B_MSIL2A_20200820T103629_N0214_R008_T31TGM_20200820T133254'

s3_folder='data/Sentinel-3/'
s3_product='S3B_SL_2_LST____20200818T100722_20200818T101022_20200819T161150_0179_042_236_2160_LN2_O_NT_004'

ext='.dim'  # Product file format

# Parameters for data_mining_sharpener.py
cv_homogeneity_threshold=0
elevation_band=elevation
lst_good_quality_flags=1
moving_window_size=15
parallel_jobs=1

# I/O file names for the sharpening pipeline
s2_reflectance=${s2_folder}${s2_product}_processed_reflectance${ext}
s2_dem=${s2_folder}${s2_product}_processed_elevation${ext}
s3_lst=${s3_folder}${s3_product}_processed_lst${ext}
s3_mask=${s3_folder}${s3_product}_processed_mask.dim
output_sharp_lst=${s3_folder}${s3_product}_sharp_lst.dim

# Run sharpening script
python data_mining_sharpener.py --high_res_reflectance ${s2_reflectance} --low_res_lst ${s3_lst} --high_res_dem ${s2_dem} --lst_quality_mask ${s3_mask} --elevation_band ${elevation_band} --lst_good_quality_flags ${lst_good_quality_flags} --cv_homogeneity_threshold ${cv_homogeneity_threshold} --moving_window_size ${moving_window_size} --parallel_jobs ${parallel_jobs} --output ${output_sharp_lst}