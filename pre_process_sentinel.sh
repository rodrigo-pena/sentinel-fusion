# ATTENTION: Change the file pointers below according to the downloaded files you actually want to explore
s2_folder='data/Sentinel-2/'
s2_product='S2B_MSIL2A_20200820T103629_N0214_R008_T31TGM_20200820T133254'

s3_folder='data/Sentinel-3/'
s3_product='S3B_SL_2_LST____20200818T100722_20200818T101022_20200819T161150_0179_042_236_2160_LN2_O_NT_004'

ext='.dim'  # Product file format

# Parameters for the SNAP pre-processing graphs
aoi='POLYGON((5.63614201613131 46.48730740760096, 6.399441865096295 46.4671492804572, 6.374261461965352 46.05871378389698, 5.616597452606011 46.07858807515982, 5.63614201613131 46.48730740760096))'  # Area Of Interest
crs=EPSG:4326  # Coordinate Reference System
pixel_res=30  # Pixel resolution (meters) to resample S2 product
max_parallel_threads=40  # Max. number of parallel threads

# I/O file names for the Sentinel-2 pre-processing pipeline
s2_input=${s2_folder}${s2_product}${ext}
output_reflectance=${s2_folder}${s2_product}_processed_reflectance${ext}
output_elevation=${s2_folder}${s2_product}_processed_elevation${ext}

# I/O file names for the Sentinel-3 pre-processing pipeline
s3_input=${s3_folder}${s3_product}${ext}
output_mask=${s3_folder}${s3_product}_processed_mask${ext}
output_lst=${s3_folder}${s3_product}_processed_lst${ext}

# Run the Sentinel-2 product through its pre-processing pipeline
gpt snap_graphs/sentinel_2_pre_processing.xml -Pinput=${s2_input} -Paoi="${aoi}" -Pcrs=${crs} -Ppixel_res=${pixel_res} -Poutput_reflectance=${output_reflectance} -Poutput_elevation=${output_elevation} -q ${max_parallel_threads}

# Run the Sentinel-3 product through its preprocessing pipeline
gpt snap_graphs/sentinel_3_pre_processing.xml -Pinput=${s3_input} -Paoi="${aoi}" -Pcrs=${crs} -Poutput_mask=${output_mask} -Poutput_lst=${output_lst} -q ${max_parallel_threads}
