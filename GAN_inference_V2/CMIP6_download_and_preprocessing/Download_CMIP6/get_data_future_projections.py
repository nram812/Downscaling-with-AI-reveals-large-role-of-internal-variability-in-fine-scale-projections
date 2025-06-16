from pathlib import Path
import glob
import pandas as pd
import os
import wget
import sys
sys.path.append(r'/nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM/get-data')
from file_downloader import FileDownloader


output_path = r'//nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM'
varnames =['ua','va','ta','zg','hus','psl']
ssp = 'ssp370'
freq ='6hrPlevPt'


def create_dict(varname, variant = 'r1i1p1f1',
                ssp = ssp, freq =freq):
    if '6hr' in freq:

        dict_download = {
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_201501010000-202101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_201501010000-202101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_202101010600-203101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_202101010600-203101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_203101010600-204101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_203101010600-204101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_204101010600-205101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_204101010600-205101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_205101010600-206101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_205101010600-206101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_206101010600-207101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_206101010600-207101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_207101010600-208101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_207101010600-208101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_208101010600-209101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_208101010600-209101010000.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_209101010600-210101010000.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_209101010600-210101010000.nc',

         }
    else:
        dict_download = {
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20150101-20201231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20150101-20201231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20210101-20301231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20210101-20301231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20310101-20401231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20310101-20401231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20410101-20501231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20410101-20501231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20510101-20601231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20510101-20601231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20610101-20701231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20610101-20701231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20710101-20801231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20710101-20801231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20810101-20901231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20810101-20901231.nc',
        f'{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20910101-21001231.nc': f'http://noresg.nird.sigma2.no/thredds/fileServer/esg_dataroot/cmor/CMIP6/ScenarioMIP/NCC/NorESM2-MM/{ssp}/{variant}/{freq}/{varname}/gn/v20200218/{varname}_{freq}_NorESM2-MM_{ssp}_{variant}_gn_20910101-21001231.nc',

         }
    return dict_download


for varname in varnames:
    if not os.path.exists(f'{output_path}/{varname}/{freq}/{ssp}'):
        os.makedirs(f'{output_path}/{varname}/{freq}/{ssp}')
        os.chdir(f'{output_path}/{varname}/{freq}/{ssp}')
    os.chdir(f'{output_path}/{varname}/{freq}/{ssp}')
    # instantiate the downloader instance
    dict_ = create_dict(varname=varname)
    downloader = FileDownloader(max_threads=7)

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
freq ='day'
files = glob.glob(f'//nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM/*/{freq}/ssp370/*.nc',
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



