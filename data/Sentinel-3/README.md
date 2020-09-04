# Sentinel-3 preprocessing steps

This file details the steps needed to go from the Sentinel-3 products downloaded from the Copernicus Open Science Hub all the way to the final grayscale image to be used in the data fusion process with the Sentinel-2 product.

You should follow these steps **after** going through the corresponding ones for the Sentinel-2 data, detailed in `sentinel-fusion/data/Sentinel-2/README.md`.



## 1. Download Sentinel-3 data

Sentinel-3 data will be downloaded together with Sentinel-2 data after running the Python script `download-sentinel-data.py`. After running the script, you should have a number of folders within `sentinel-fusion/data/Sentinel-3/` with the suffix `.SEN3`.



## 2. Reproject and subset

Typically, the downloaded Sentinel-3 data will include more dates than the downloaded Sentinel-2 data. This is because Sentinel-2 covers the globe in about 5 days, whereas Sentinel-3 does so every day. Thus, you must pick among the downloaded Sentinel-3 folders the ones with dates that are closer to the Sentinel-2 products that you have. Select those folders and drag them into the "Product Explorer" box within the SNAP application  to open up the corresponding Sentinel products. 

Explore the `LST_uncertainty` bands for the opened products, keep open the one with lower uncertainty for the area that you are interested in, and close the remaining ones.

Now we need to reproject the Sentinel-3 measurements so that they align with the optical measurements in the mosaic that you created for Sentinel-2. Open the `.dim` mosaic file (that you created after following `sentinel-fusion/data/Sentinel-2/README.md`) by dragging it into the "Product Explorer" box within SNAP. Then, click on `Raster > Geometric Operations > Reprojection` and follow these steps: 

1. Under `I/O Parameters`, select as source products all the Sentinel-3 product. Choose a name for the output file and make sure that the save directory is marked as `sentinel-fusion/data/Sentinel-3/`. It's a good idea to also leave the option `Open in SNAP` checked to automatically open the resulting mosaic product in the end.
2. Under `Reprojection Parameters`, select `Use CRS of:` and point to the Sentinel-2 mosaic product as reference. 
3. Ensure that `Reproject tie-point grids` is checked, and that the `Resampling method: Nearest` is chosen.
4. Hit `Run` and wait for the process to complete.



## 4. Export the LST band as a greyscale image

The reprojected product should be open now. If not, simply go to the directory `sentinel-fusion/data/Sentinel-3/` and drag and drop the corresponding `.dim`  file onto the `Product Explorer` box within SNAP.

Navigate to `Bands > LST` within the reprojected product and double click on it to open it in a new window. Then, right-click on the view and select `Export View as Image`. Under `Image Region`, select `Full scene`, and pick the save directory as `sentinel-fusion/data/Sentinel-3/`. Finally, set GeoTIFF as file type, pick a file name and hit `Save`.



