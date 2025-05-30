# Super-greenhouse trends

Notebooks for data analysis and plots related to the paper: 
C. Abraham, M. Dewey, and C. Goldblatt (in prep). Trends in the occurrence and strength of super-greenhouse conditions over tropical oceans. Geophysical Research Letters. 

## Data

Satellite data is available freely for download: AIRS data is available from The Goddard Earth Sciences Data and Information Services Center (GES-DISC) at NASA (https://disc.gsfc.nasa.gov), and CERES data is available from the Langley Research Center (LARC) at NASA (https://ceres.larc.nasa.gov/). This repository and the pre-processed data is also archived here: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15527946.svg)](https://doi.org/10.5281/zenodo.15527946)

## Code

edata_cred.py will setup credentials to download data from the NASA servers.  
sge_data_prep.ipynb will process the raw satellite data (once already downloaded)  
sge_paper_finalplots.ipynb will create all figures in the paper  
Note that the pre-processed data and some CERES files required to make the figures are hosted on zenodo, but are too large to be included on github.
