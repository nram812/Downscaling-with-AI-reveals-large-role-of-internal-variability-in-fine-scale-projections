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


# Directory structure: /nesi/project/niwa02916/synda_home/data/CMIP6
# Directory structure: /nesi/project/niwa02916/synda_home/data/CMIP6/ScenarioMIP/AWI/AWI-CM-1-1-MR/ssp585/r1i1p1f1/Amon/ua/gn/v20190529
# 'https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/CMIP/NCC/NorESM2-MM/historical/r1i1p1f1/6hrPlev/hus/gn/v20191108/hus_6hrPlev_NorESM2-MM_historical_r1i1p1f1_gn_197001010300-197912312100.nc'
# 'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/historical/r1i1p1f1/day/hus/gn/v20200218/hus_day_NorESM2-MM_historical_r1i1p1f1_gn_20910101-21001231.nc'
file_size_thres = 3 * 1e9 # filethreshold of 3 gigbytes
output_path = r'/nesi/nobackup/niwa00018/CMIP6_data/download-cmip6/test'
# variables to download
varnames =['ua','va','ta','wap','hus']
# ssp patterns
ssp = 'historical'
freq ='day'

sys.path.append(r'/nesi/nobackup/niwa00018/CMIP6_data/download-cmip6/get-data')
from file_downloader import FileDownloader


def create_outputpath(link, output_path):
    link_subset = link.split('CMIP6')[-1]
    paths = Path(link1)
    output_paths = f'{output_path}/CMIP6{paths.parent}'
    if not os.path.exists(output_paths):
        os.makedirs(output_paths)



def create_dict(varname, variant = 'r1i1p1f1',
                ssp = ssp, freq =freq):
    if '6hr' in freq:

        dict_download = {f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_195001010300-195912312100.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_195001010300-195912312100.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_196001010300-196912312100.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_196001010300-196912312100.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_197001010300-197912312100.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_197001010300-197912312100.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_198001010300-198912312100.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_198001010300-198912312100.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_199001010300-199912312100.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_199001010300-199912312100.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_200001010300-200912312100.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_200001010300-200912312100.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_201001010300-201412312100.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_201001010300-201412312100.nc'
         }
    else:
        dict_download = {f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19500101-19591231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19500101-19591231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19600101-19691231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19600101-19691231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19700101-19791231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19700101-19791231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19800101-19891231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19800101-19891231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19900101-19991231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_19900101-19991231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20000101-20091231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20000101-20091231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20100101-20141231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/CMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20191108/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20100101-20141231.nc'
         }
    return dict_download


for varname in varnames:
    if not os.path.exists(f'{output_path}/{varname}/{freq}/{ssp}'):
        os.makedirs(f'{output_path}/{varname}/{freq}/{ssp}')
        os.chdir(f'{output_path}/{varname}/{freq}/{ssp}')
    os.chdir(f'{output_path}/{varname}/{freq}/{ssp}')
    # instantiate the downloader instance
    dict_ = create_dict(varname=varname)
    downloader = FileDownloader(max_threads=35)

    counter = 0
    for filename,link in dict_.items():

        #print(filename, link)

        if not os.path.exists(f'{output_path}/{varname}/{freq}/{ssp}/{filename}'):
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
        #         downloader.get_file(link, filename)'


# Determines the approximated speed

import glob
import time
import pathlib as p

files = glob.glob(f'//nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM/*/{freq}/historical/*.nc',
                  recursive=True)

size = [p.Path(file).stat().st_size for file in files]
initial_size = sum(size)
print(initial_size/1e9)
start = time.time()
n_seconds = 10
time.sleep(n_seconds)
size = [p.Path(file).stat().st_size for file in files]
final_size = sum(size)

print(((final_size - initial_size)/n_seconds)/1e6)
# This is

