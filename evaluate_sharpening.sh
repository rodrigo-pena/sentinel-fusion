# ATTENTION: Change the file pointers below according to the downloaded files you actually want to explore
landsat_folder='data/Landsat/'
landsat_product='LC08_L1TP_196028_20200818_20200823_01_T1'
landsat_product_path=${landsat_folder}${landsat_product}/

s3_folder='data/Sentinel-3/'
s3_product='S3B_SL_2_LST____20200818T100722_20200818T101022_20200819T161150_0179_042_236_2160_LN2_O_NT_004'

ext='.dim'  # Product file format

# Parameters for evaluate_sharpening.py
save_residuals=True

# I/O file names for the evaluation pipeline
low_res_lst=${s3_folder}${s3_product}_processed_lst${ext}
sharp_lst=${s3_folder}${s3_product}_sharp_lst${ext}
gt_high_res_lst=${landsat_product_path}${landsat_product}_processed_lst${ext}
output_residual=${s3_folder}${s3_product}_sharpening_landsat_residuals${ext}

# Run evaluation script
python evaluate_sharpening.py --low_res_lst ${low_res_lst} --sharp_lst ${sharp_lst} --gt_high_res_lst ${gt_high_res_lst} --save_residuals ${save_residuals} --output_residual=${output_residual}