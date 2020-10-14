# Parameters for convert_landsat_tir_to_lst.py
landsat_product_path='data/Landsat/LC08_L1TP_196028_20200818_20200823_01_T1'
lst_output='data/Landsat/LC08_L1TP_196028_20200818_20200823_01_T1/LC08_L1TP_196028_20200818_20200823_01_T1_LST.TIF'
band_number=10

# Run convert_landsat_tir_to_lst.py
python convert_landsat_tir_to_lst.py --landsat_product_path ${landsat_product_path} --lst_output ${lst_output} --band_number ${band_number}