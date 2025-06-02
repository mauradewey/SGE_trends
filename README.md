# Super-greenhouse trends

Notebooks for data analysis and plots related to the paper: 
C. Abraham, M. Dewey, and C. Goldblatt. Trends in the occurrence and strength of super-greenhouse conditions over tropical oceans.  

## Data

All satellite data used in this study is freely available for download. AIRS data is available from The Goddard Earth Sciences Data and Information Services Center at NASA (https://disc.gsfc.nasa.gov/datasets/AIRS3STD_7.0/summary?keywords=AIRS). CERES data is available from the Langley Research Center at NASA (https://ceres-tool.larc.nasa.gov/ord-tool/jsp/SSF1degEd41Selection.jsp). This repository and the pre-processed data is also archived here: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15527946.svg)](https://doi.org/10.5281/zenodo.15527946)

## Code

edata_cred.py will setup credentials to download data from the NASA servers.  
sge_data_prep.ipynb will process the raw satellite data (once already downloaded)  
sge_paper_finalplots.ipynb will create all figures in the paper (the files required are already included in the repository)  
Note that the processed satellite data (SGE_timeseries_2002_2023_v7.nc) and some CERES files required to make the figures are hosted on zenodo, but are too large to be included on github.
