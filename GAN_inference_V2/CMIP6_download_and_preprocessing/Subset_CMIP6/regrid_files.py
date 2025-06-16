import glob
import json
import os
import glob
import sys
from subprocess import call
from concurrent.futures import ProcessPoolExecutor, as_completed, wait
import pandas as pd
import numpy as np
import pathlib
base_dir = r'/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive/CMIP6'

experiments = ['CMIP', 'ScenarioMIP'] # this the scenarios 
variables = ['hus','ua','va', 'ta']
target_grid = '/nesi/project/niwa00018/rampaln/downscaling-ccam/subset_ccam/target_grid.csv'
gcm = str(sys.argv[-1])
ssp = str(sys.argv[-2])
variant = str(sys.argv[-3])
output_dir = str(sys.argv[-4])
print(gcm, ssp, variant)
# output_dir = '/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/Downscaled_Preprocessed'
# gcm = 'EC-Earth3'
# ssp = 'ssp126'


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

def get_files(gcm, ssp, variant, output_dir = output_dir):
    if 'ssp' in ssp:
        files = f'/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive/CMIP6/ScenarioMIP/*/{gcm}/{ssp}/{variant}/day/*/*/*/*.nc'
    else:
        files = f'/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive/CMIP6/CMIP/*/{gcm}/{ssp}/{variant}/day/*/*/*/*.nc'
    files = glob.glob(files, recursive =True)
    print(files)
    filename = files[0].split('/')[-1]
    output_path = f"{output_dir}{files[0].split('/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive/CMIP6')[1]}".split(filename)[0]  
    varname_output = output_path.split('/')[-4]
    output_path = output_path.replace(varname_output, 'tmp')
    output_path = [output_path] * len(files)

    return files, output_path




def regrid_files(files, output_path, target_grid, variables = variables):
    nprocs = 40  # specify number of processors to use (depends on node)
    pool = ProcessPoolExecutor(nprocs)
    tasks = []  # list for references to submitted jobs
    # levels for extraction
    vname = '85000,50000,25000'
    variable_name = []
    fnames = []
    for i, file in enumerate(files):
        #print(file)
        if file.split('/')[-1].split('_')[0] in variables:
            fname = f'{output_path[i]}' + f'/{file.split("/")[-1]}'
            if not os.path.exists(output_path[i]):
                os.makedirs(output_path[i])
                print(f"made outputdir: {output_path[i]}")
            fnames.append(fname)
            variable_name.append(file.split('/')[-4])
            #print(output_path[i])
            if not os.path.exists(fname):
                arg = f'cdo -L -sellevel,{vname} -remapcon,{target_grid} {file} {fname}'
                print(f'saving file to : {fname}')
                #print(arg)
                task = pool.submit(call, arg, shell=True)
                tasks.append(task)
        

    for task in as_completed(tasks):  # helps see as tasks are completed
        print(task.result())
    return fnames, variable_name

 # gcm OPTIONS
files, output_paths = get_files(gcm, ssp, variant)
print(files)
files_to_check, variable_name = regrid_files(files, output_paths, target_grid)
# create a dataframe with all the file that 'should have been interpolate'
file_list = pd.DataFrame( np.vstack([files_to_check, variable_name]), index = None,).T
file_list.to_csv(f'{output_dir}/{gcm}_{ssp}_{variant}.csv')




