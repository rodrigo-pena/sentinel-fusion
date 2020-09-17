# sentinel-fusion

Fusing data from the ESA Copernicus Programme's Sentinel missions.

This repository implements code to increase the resolution of the Land Surface Temperature (LST) band of Sentinel-3 by exploiting the higher resolution visible spectrum bands of Sentinel-2.

## 1. Setup

*Warning*: these instructions have been tested on a macOS Catalina Version 10.15.6. You might have to adapt the steps below according to your system.

To be able to run the programs locally, first download or clone this repository to your local system, placing it at a location that I will refer to as `<repository_dir>`. Then, follow the steps below.

### 1. Create a conda environment

Open a Terminal window, navigate to `<repository_dir>`, and run

```sh
conda create --name sentinel-fusion python=3.6
```

to create the environment `sentinel-fusion` (you can also use any other name that you like). Then, remember to activate the environment, *i.e.*,

```sh
conda activate sentinel-fusion
```

every time you want to call a program from the repository.

### 2. Install SNAP

Go to the the [SNAP download page][snap-download] and download and install the Sentinel Toolboxes on your system. You have to setup the snappy Python module for use within the `sentinel-fusion` conda environment. It might be possible to setup snappy for your system at the end of the Sentinel Toolboxes installation, but for macOS Catalina I had to resort to the instructions I have detailed in [snappy_config_catalina.md][snappy_config_catalina.md]. You also have to make sure that you can call the SNAP Graph Processing Tool (GPT) command line interface. To check that this is the case, open the Terminal, run

```sh
gpt -h
```

and observe if the output starts with 

```
Usage:
  gpt <op>|<graph-file> [options] [<source-file-1> <source-file-2> ...]

Description:
  This tool is used to execute SNAP raster data operators in batch-mode. The operators can be used stand-alone or combined as a directed acyclic graph (DAG). Processing graphs are represented using XML. More info about processing graphs, the operator API, and the graph XML format can be found in the SNAP documentation.
```

### 3. Install pyDMS

Download or clone [pyDMS][pydms], a Python Data Mining Sharpener implementation, into a location `<pyDMS_dir>` in your local system. To install it, open a Terminal window, navigate to `<pyDMS_dir>`, make sure that you are within the `sentinel-fusion` environment, and run

```sh
python setup.py install
```

### 4. Install the remaining dependencies

Run 

```sh
pip install -r requirements.txt
```

## 2. Data download

The Python script `sentinel_data_download.py` coordinates the download of Sentinel-2 and Sentinel-3 products. Type 

```sh
python sentinel_data_download.py --help
```

on the Terminal for usage information. You can also simply open the Terminal and run 

```sh
sh sentinel_data_download.sh
```

to download a default dataset. After running `sentinel_data_download.py`, you should have `.SAFE` folders in `data/Sentinel-2` and `.SEN3` folders in `data/Sentinel-3`. These folders are called, respectively, Sentinel-2 and Sentinel-3 products.

## 3. Pre-processing

Open the Terminal and run

```sh
sh sentinel_write_dim.sh
```

to save the default Sentinel products as BEAM-DIMAP files. These files are needed for the pre-processing programs. Then, run

```sh
sh sentinel_pre_processing.sh
```

to pre-process the default Sentinel products. In doing so, you will create the set of BEAM-DIMAP files that the LST sharpening procedure needs.

If you want to use data other than the default, check the contents of the scripts [sentinel_write_dim.sh](sentinel_write_dim.sh) and  [sentinel_pre_processing.sh](sentinel_pre_processing.sh) to see what commands you need to issue. Essentially, you can simply make copies of these two scripts and change the names of the Sentinel products that the copies point to.

Please note that the pre-processing step may take a while.

You can view the processed Sentinel-2 reflectance and Sentinel-3 lst BEAM_DIMAP products on SNAP. You should be able to generate for them views like the following, respectively:

![High Resolution Visible Spectrum](/images/thumbnail_hr_visible.png)

![Low Resolution LST](/images/thumbnail_lr_lst.png)

## 4. LST sharpening

After the pre-processing is done, you can run 

```sh
sh data_mining_sharpener.sh
```

on the Terminal to get a sharpened LST using the default Sentinel products. The sharpened LST will be saved as a BEAM-DIMAP file that you can browse on SNAP. The view of its LST band should be something like this:

![High Resolution LST](/images/thumbnail_hr_lst.png)

Check the scripts [data_mining_sharpener.sh](data_mining_sharpener.sh) and [data_mining_sharpener.sh](data_mining_sharpener.sh) for inspiration on how you can adapt the program's arguments for your own purposes.

## Acknowledgements

This work was done in the context of a project with [GRID-Geneva][grid-geneva].

Some of the scripts in this repository are based on the ones in https://github.com/DHI-GRAS/sen-et-snap-scripts/, produced by the [Sen-ET project][sen-et-webpage] team.

## License

The content is released under the terms of the [GNU General Public License](LICENSE).



[sen-et-webpage]: http://esa-sen4et.org/
[grid-geneva]: https://unepgrid.ch/en
[pydms]: https://github.com/radosuav/pyDMS

