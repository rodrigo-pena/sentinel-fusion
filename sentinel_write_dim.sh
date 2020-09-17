# ATTENTION: Change the file pointers below according to which downloaded files you actually want to explore
s2_folder='data/Sentinel-2/'
s2_product='S2A_MSIL2A_20200805T104031_N0214_R008_T31TGM_20200805T121101.SAFE'
s3_folder='data/Sentinel-3/'
s3_product='S3A_SL_2_LST____20200805T094312_20200805T094612_20200806T151948_0179_061_193_2160_LN2_O_NT_004.SEN3'
max_parallel_threads=40

# Write Sentinel-2 .SAFE product to BEAM-DIMAP
gpt Write -Ssource=${s2_folder}${s2_product} -Pfile=${s2_folder}${s2_product/%.*/.dim} -q ${max_parallel_threads}

# Write Sentinel-3 .SAFE product to BEAM-DIMAP
gpt Write -Ssource=${s3_folder}${s3_product} -Pfile=${s3_folder}${s3_product/%.*/.dim} -q ${max_parallel_threads}