import wget
import pandas as pd
import requests
import numpy as np
from tqdm import tqdm
import requests
from multiprocessing.dummy import Pool as ThreadPool
import urllib
import os
import os, sys, threading
import requests
from pathlib import Path
import glob
import pandas as pd
import os
import wget
file_size_thres = 3 * 1e9 # filethreshold of 3 gigbytes
output_path = r'//nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM'
varnames =['va','ta','zg','hus']
ssp = 'historical'
'https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/CMIP/NCC/NorESM2-MM/historical/r1i1p1f1/6hrPlev/hus/gn/v20191108/hus_6hrPlev_NorESM2-MM_historical_r1i1p1f1_gn_197001010300-197912312100.nc'
sys.path.append(r'/nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM/get-data')
from file_downloader import FileDownloader

def create_dict(varname, variant = 'r1i1p1f1', ssp = ssp):
    dict_download = {f'{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_195001010300-195912312100.nc': f'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/6hrPlevPt/{varname}/gn/v20191108/{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_195001010300-195912312100.nc',
    f'{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_196001010300-196912312100.nc': f'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/6hrPlevPt/{varname}/gn/v20191108/{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_196001010300-196912312100.nc',
    f'{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_197001010300-197912312100.nc': f'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/6hrPlevPt/{varname}/gn/v20191108/{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_197001010300-197912312100.nc',
    f'{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_198001010300-198912312100.nc': f'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/6hrPlevPt/{varname}/gn/v20191108/{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_198001010300-198912312100.nc',
    f'{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_199001010300-199912312100.nc': f'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/6hrPlevPt/{varname}/gn/v20191108/{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_199001010300-199912312100.nc',
    f'{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_200001010300-200912312100.nc': f'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/6hrPlevPt/{varname}/gn/v20191108/{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_200001010300-200912312100.nc',
    f'{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_201001010300-201412312100.nc': f'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/6hrPlevPt/{varname}/gn/v20191108/{varname}_6hrPlevPt_NorESM2-MM_{ssp}_{variant}_gn_201001010300-201412312100.nc'
     }
    return dict_download


for varname in varnames:
    if not os.path.exists(f'{output_path}/{varname}/{ssp}'):
        os.makedirs(f'{output_path}/{varname}/{ssp}')
        os.chdir(f'{output_path}/{varname}/{ssp}')
    os.chdir(f'{output_path}/{varname}/{ssp}')
    # instantiate the downloader instance
    dict_ = create_dict(varname=varname)
    downloader = FileDownloader(max_threads=25)

    counter = 0
    for filename,link in dict_.items():

        #print(filename, link)

        if not os.path.exists(f'{output_path}/{varname}/{ssp}/{filename}'):
            print("downloading file didn't exist already", filename)
            counter += 1
            z = 1
            downloader.get_file(link, filename)
        # else:
        #     if (Path(f'{output_path}/{varname}/{filename}').stat().st_size < file_size_thres) & \
        #             (Path(f'{output_path}/{varname}/{filename}').stat().st_size > 1e1):
        #         print("File did exist, now removing existing one and re-downloading",filename)
        #         # Delete the path and redownload the data
        #         os.remove(f'{output_path}/{varname}/{filename}')
        #         counter += 1
        #         downloader.get_file(link, filename)

