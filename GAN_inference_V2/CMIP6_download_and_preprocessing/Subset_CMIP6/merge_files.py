import os
import glob
import json
import os
import glob
import sys
from subprocess import call
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed, wait
import pandas as pd
import pathlib
base_dir = r'/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive/CMIP6'
output_dir = '/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/Downscaled_Preprocessed'
experiments = ['CMIP', 'ScenarioMIP']
variables = ['hus','ua','va', 'ta']
target_grid = '/nesi/project/niwa00018/rampaln/downscaling-ccam/subset_ccam/target_grid.csv'
gcm = str(sys.argv[-1])
ssp = str(sys.argv[-2])
variant = str(sys.argv[-3])
output_dir = str(sys.argv[-4])
forced_override = False


"""['CESM2-WACCM',
 'UKESM1-0-LL',
 'AWI-CM-1-1-MR',
 'IITM-ESM',
 'CanESM5',
 'MPI-ESM1-2-HR',
 'INM-CM5-0',
 'INM-CM4-8',
 'TaiESM1',
 'EC-Earth3',
 'MRI-ESM2-0',
 'ACCESS-CM2',
 'MIROC6',
 'IPSL-CM6A-LR',
 'NorESM2-LM',
 'NorESM2-MM',
 'MPI-ESM1-2-LR']"""

def merge_files(files_to_merge, varname, gcm, ssp):
    #print(files_to_merge.iloc[0],"chur")
    output_fname = files_to_merge.iloc[0].replace(f'{files_to_merge.iloc[0].split("/")[-1]}', '')
    output_file = f"{output_fname}/{gcm}_{ssp}_{varname}.nc"
    files = ' '.join(files_to_merge)
    cdo_command = f'cdo mergetime {files} {output_file}'
    return cdo_command, output_file

# mssing filelist 

file_list = pd.read_csv(f'{output_dir}/{gcm}_{ssp}_{variant}.csv', index_col =0)
counter = 0
missing_files = []
for file in file_list["0"]:
    if os.path.exists(file):
        counter+=1
        print("chur")
    else:
        print("fuck")
        missing_files.append(file)
print(missing_files, len(missing_files))
missing_files = pd.DataFrame(missing_files)
if (len(missing_files) >0):
    print("no missing data, fuck")
    missing_files.to_csv((f'{output_dir}/{gcm}_{ssp}_{variant}_missing.csv'))
# Only if all files exist
if (counter == len(file_list))|(forced_override):
    hus, output_fname_hus = merge_files(file_list["0"][file_list["1"] =='hus'],'hus', gcm, ssp)
    ta, output_fname_ta = merge_files(file_list["0"][file_list["1"] =='ta'], 'ta', gcm, ssp)
    va, output_fname_va = merge_files(file_list["0"][file_list["1"] =='va'], 'va', gcm, ssp)
    ua, output_fname_ua = merge_files(file_list["0"][file_list["1"] =='ua'],'ua', gcm, ssp)
    fnames = [output_fname_hus, output_fname_ta,  output_fname_va, output_fname_ua]
    dframe = pd.DataFrame(fnames, index = None)
    print(dframe, f'{output_dir}/{gcm}_{ssp}_{variant}_mergefiles.csv')
    dframe.to_csv(f'{output_dir}/{gcm}_{ssp}_{variant}_mergefiles.csv')

    try:
        subprocess.run(hus, shell=True, check=True)
        subprocess.run(ta, shell=True, check=True)
        subprocess.run(va, shell=True, check=True)
        subprocess.run(ua, shell=True, check=True)
        print(f"Successfully merged files into {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


else:
    print("missing files")



# Run the command using subprocess

    






