# ATTENTION: Change the file pointers below according to the downloaded files you actually want to explore
landsat_folder='data/Landsat/'
landsat_product='LC08_L1TP_196028_20200818_20200823_01_T1'
landsat_product_path=${landsat_folder}${landsat_product}/

ext='.dim'  # Product file format

# Parameters for landsat_tir_to_lst.py
band_number=10  # TIR band to use

# Parameters for the SNAP pre-processing graph
aoi='POLYGON((5.63614201613131 46.48730740760096, 6.399441865096295 46.4671492804572, 6.374261461965352 46.05871378389698, 5.616597452606011 46.07858807515982, 5.63614201613131 46.48730740760096))'  # Area Of Interest
band_name=LST
crs=EPSG:4326  # Coordinate Reference System
max_parallel_threads=40  # Max. number of parallel threads
pixel_res=30  # Pixel resolution (meters) to resample S2 product

# I/O file names for the Landsat pre-processing pipeline
lst_output=${landsat_product_path}${landsat_product}_lst${ext}
processed_lst_output=${landsat_product_path}${landsat_product}_processed_lst${ext}

# Convert TIR band to LST
python landsat_tir_to_lst.py --landsat_product_path ${landsat_product_path} --lst_output ${lst_output} --band_number ${band_number}

# Run the Sentinel-3 product through its preprocessing pipeline
gpt snap_graphs/landsat_lst_pre_processing.xml -Pinput=${lst_output} -Paoi="${aoi}" -Pcrs=${crs} -Pband_name=${band_name} -Poutput=${processed_lst_output} -q ${max_parallel_threads}
