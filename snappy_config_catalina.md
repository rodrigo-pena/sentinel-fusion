# How to configure snappy for macOS Catalina

## 1. Install SNAP

Download the `.dmg` file it from [here](http://step.esa.int/main/download/snap-download/), open it and follow the standard installation instructions. In the last window ("Select Python"), **uncheck** the option "Configure SNAP for use with Python".

## 2. Build a jpy wheel

Go to https://github.com/bcdev/jpy  and https://jpy.readthedocs.io/en/latest/install.html to follow the instructions to generate the `.whl` file under `jpy/dist/`. Copy this wheel to the directory `~/.snap/snap-python/snappy/`.

## 3. Uninstall all your current JDK

Follow the instructions [here](https://docs.oracle.com/javase/10/install/installation-jdk-and-jre-macos.htm#JSJIG-GUID-F9183C70-2E96-40F4-9104-F3814A5A331F)

## 4. Install the legacy Java 6 runtime

Download the `.dmg` file [here](https://support.apple.com/kb/DL1572?locale=en_US) and then run the following in the Terminal (as first explained [here](https://apple.stackexchange.com/questions/375973/java-uninstalled-but-still-cannot-install-java-6-macos)):

```sh
t=${TMPDIR:-/tmp}/java
hdiutil mount </path/to/JavaForOSX.dmg>
pkgutil --expand /Volumes/Java\ for\ macOS\ 2017-001/JavaForOSX.pkg "$t"
hdiutil unmount /Volumes/Java\ for\ macOS\ 2017-001
sed -i '' 's/return false/return true/g' "$t"/Distribution
pkgutil --flatten "$t" ~/Desktop/Java.pkg
rm -rf "$t"
open ~/Desktop/Java.pkg
```

## 5. Install snappy

Go to  `~/.snap/snap-python/snappy/` in the Terminal and run (under your desired environment)

```sh
python setup.py install
```

If everything goes right the Python code

```python
from snappy import ProductIO
p = ProductIO.readProduct('snappy/testdata/MER_FRS_L1B_SUBSET.dim')
list(p.getBandNames())
```

should return

```sh
['radiance_1', 'radiance_2', 'radiance_3', 'radiance_4', 'radiance_5', 'radiance_6', 'radiance_7', 'radiance_8', 'radiance_9', 'radiance_10', 'radiance_11', 'radiance_12', 'radiance_13', 'radiance_14', 'radiance_15', 'l1_flags', 'detector_index']
```
