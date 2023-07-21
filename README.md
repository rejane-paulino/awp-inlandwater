# (AWP - Inland Water) Adaptative Window by Proportion applied to Inland Water <img src="img/awpinlandwater.svg" width="150" align="right" />
![Version](https://img.shields.io/badge/version-v0.0.1-blue)
![License](https://img.shields.io/badge/license-GPL%203.0-blue)
![Language](https://img.shields.io/badge/language-Python-blue)

AWP-Inland Water is a proto-algorithm that has been developed to address the reduction of adjacency effect on satellite-imagery applied to small waterbodies. The key principle behind AWP-Inland Water lies in its ability to adapt window-ranges according to local conditions across the waterbodies. For more details about this proto-algorithm, we recommend referring to the comprehensive study conduced by Paulino et al. (2022).   

## Requirements and Usage:

AWP-Inland Water is coded in Python 3.8 and it requires Python packages to run: `numpy`, `pandas`, `gdal`, `cv2`, `py6S`, `xmltodict`, `cython`. 

To run the AWP-Inland Water, it is necessary a suitable use of the environment `awp` by command line:

            conda env create -f environment.yml
            conda activate awp
            cd into the awp-inlandwater directory
            python api.py

## Input Parameters:
* *path_image*: folder where the images are available (string);
* *path_output*: folder where the corrected images will be saved (string);
* *path_metadata*: path with image metadata (e.g., MTL.xml) (string);
* *aod_value*: AOD (Aerosol Optical Depth) value (float);
* *target_altitude_value*: altitude value in km (float);
* *p_min_value*: minimum proportion value of non-water targets within range (float, from 0 to 100);
* *p_max_value*: maximum proportion value of non-water targets within range (float, from 0 to 100);
* *default*: True or False. If "True" the code will be ran using default values for mininum and maximum proportions of non-water targets. Otherwise, it will be ran using the values provided by users.
        
## Output Parameters:
Corrected images with 20 m of spatial resolution (.TIFF) are available in *path_output*.

## Warning:

> AWP-Inland Water is based on multi-iterations; therefore, its estimation is time-consuming. We deeply recommend to the users to divide the original image in small blocks around the waterbodies to enhance time and resources use efficiency.

## Reference:

Paulino, R.S.; Martins, V.S.; Novo, E.M.L.M.; Barbosa, C.C.F.; de Carvalho, L.A.S.; Begliomini, F.N. Assessment of Adjacency Correction over Inland Waters Using Sentinel-2 MSI Images. Remote Sens. 2022, 14, 1829. https://doi.org/10.3390/rs14081829
