# Sentinel-2 preprocessing steps

This file details the steps needed to go from the Sentinel-2 products downloaded from the Copernicus Open Science Hub all the way to the final RGB image to be used in the data fusion process with the Sentinel-3 product.



## 1. Download Sentinel-2 data

Open the Terminal, change directory to `sentinel-fusion/` and issue the command

```shell
python download-sentinel-data.py
```

to download Sentinel-2 data under `sentinel-fusion/data/Sentinel-2/` using default argument values. 

Alternatively, you can specify an Open Science Hub username/password and a planetary area-of-interest (AOI) with the following command: 

```shell
python download-sentinel-data.py -user <username> -password <password> -aoi <geojsonpath>
```

Call `python download-sentinel-data.py -h ` in the Terminal for detailed usage information. 

After running the script, you should have a number of folders within `sentinel-fusion/data/Sentinel-2/` with the suffix `.SAFE`. This is the downloaded data.



## 2. Resample the bands

The measured optical bands within the downloaded data have spatial resolution that can vary from 10m to 60m. We must resample all of them to make sure that the resolution across all bands is the same and equal to 10m.

Open up the SNAP application. Then, in your computer's file explorer, go to `sentinel-fusion/data/Sentinel-2/` and select all of the `.SAFE` folders. Drag and drop them into the "Product Explorer" box within SNAP to open up the corresponding Sentinel products.

Now open the `S2_Resampling` tool within SNAP and, for each of the loaded products, do the following:

1. Under the tab `I/O Parameters`, make sure the "Save as BEAM-DIMAP" checkbox is checked and that the save directory is `sentinel-fusion/data/Sentinel-2/`.
2. Under the tab `Processing Parameters`, choose `Output resolution: 10`, `Upsampling method: Nearest`, `Downsampling method: Median`, and leave the rest on the default values.
3. Then, press `Run` and wait for the process to be over.



## 3. Collate the different products into a mosaic

Now that all the measured bands have been resampled to the same resolution, click on `Raster > Geometric Operations > Mosaicing`. Then, 

1. Under `I/O Parameters`, select as source products all the `.dim` files that were created during the resampling step. Once again, make sure that the save directory is `sentinel-fusion/data/Sentinel-2/`. It's a good idea to also leave the option `Open in SNAP` checked to automatically open the resulting mosaic product in the end.
2. Under `Map Projection Definition`, select `Projection: UTM / WGS 84 (Automatic)` and set the pixel size on X and Y directions as 10m. Pick the mosaic bounds to be `North: 46.552`, `West: 5.692`, `East: 6.557`, and `45.923` to encompass the greater Geneva agglomeration.
3. Under `Variables & Conditions`, click the link with caption "Choose the bands to process" and select the bands B2, B3 and B4.
4. Hit `Run` and wait for the process to complete.



## 4. Export the mosaic as an RGB image

The mosaic product should be open now. If not, simply go to the directory `sentinel-fusion/data/Sentinel-2/` and drag and drop the `.dim` mosaic file that was created in the previous step onto the `Product Explorer` box within SNAP.

Right click on the mosaic product and select `Open RGB Image Window`. Once the window finishes loading, right click on the view and select `Export View as Image`. Under `Image Region`, select `Full scene`, and pick the save directory as `sentinel-fusion/data/Sentinel-2/`. Then, pick GeoTIFF as file type, pick a file name and hit `Save`.



