# ATTENTION: Change the file pointers below according to which downloaded files you actually want to explore
s2_folder='data/Sentinel-2/'
s2_product='S2B_MSIL2A_20200820T103629_N0214_R008_T31TGM_20200820T133254.SAFE'
s3_folder='data/Sentinel-3/'
s3_product='S3B_SL_2_LST____20200818T100722_20200818T101022_20200819T161150_0179_042_236_2160_LN2_O_NT_004.SEN3'
max_parallel_threads=40

# Write Sentinel-2 .SAFE product to BEAM-DIMAP
gpt Write -Ssource=${s2_folder}${s2_product} -Pfile=${s2_folder}${s2_product/%.*/.dim} -q ${max_parallel_threads}

# Write Sentinel-3 .SAFE product to BEAM-DIMAP
gpt Write -Ssource=${s3_folder}${s3_product} -Pfile=${s3_folder}${s3_product/%.*/.dim} -q ${max_parallel_threads}