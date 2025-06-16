import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import requests
from multiprocessing.dummy import Pool as ThreadPool
import urllib
import pathlib
import os, sys, threading
sys.path.append(r'/nesi/nobackup/niwa00018/CMIP6_data/download-cmip6/get-data')
#sys.path.append(r'./get-data')

from file_downloader import FileDownloader
from scrape_links import *
sys.path.append("/nesi/project/niwa00004/rampaln/conda_pkg_dir/lib/python3.6/site-packages")

import requests
from pathlib import Path
import glob
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
import time
import os
import wget
import httplib2
import swifter
#import logging
import argparse
parser = argparse.ArgumentParser(description='Download CMIP6 Data')

parser.add_argument('-v','--variables', help='variables to download', required=False, default=['ta','hus','ua','va'])
parser.add_argument('-s','--ssps', help='ssps to download', required=False, default='historical')
parser.add_argument('-o','--output_path', help='output path for data', required=False, default='/nesi/nobackup/niwa03712/rampaln/CMIP6_archive')
parser.add_argument('-w','--wget', help='wget file (sh)', required=True)
parser.add_argument('-w_var','--wget_var', help='wget variable obtained from esgf', required=True)
parser.add_argument('-w_ssp','--wget_ssp', help='wget ssp obtained from esgf', required=True)
parser.add_argument('-n','--threads', help='Number of threads', required=False, default=20)
args = vars(parser.parse_args())

# extract variables from the argument parser
variables = list(args['variables'])
ssps = args['ssps']
if ssps =="ssp":
    ssps = ["ssp370"]
else:
    ssps = ["historical"]

output_path = args['output_path']
path = r'./WGETs/'
name = args["wget"]
wget_variable = args["wget_var"]
ssp = args["wget_ssp"]
#variables = ['ta','hus','ua','va']
#variables = ['pr','tasmax','tasmin','sfcWind']
variables = ['tas', 'psl']
# manual override for testing
# output_path = "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive"
# path = r'./WGETs/'
# name = "CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3/CMIP6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3.ssp126.r1i1p1f1.day.hus.gr.sh"
# wget_variable = "hus"
# ssp = "ssp370"
# import the modules

links = Scrape_WGET(path+name,wget_variable,ssp, startdate=1950, enddate=2100,
                variables=variables, ssps=ssps)
links = pd.melt(links, id_vars =['variables','ssps'])
links = links.swifter.apply(lambda a: [i.strip("'") for i in a])
print(links.value)

down_start = time.time()
downloader = FileDownloader(max_threads=int(args["threads"]))
# download the files
outpath, size, downloading = download_list(downloader, links, output_path)
down_end = time.time()
print('Download Time:',down_end-down_start)
print('Downloaded:',len(size),'Files, with a size of:',np.sum(size)/1e9,'GB')
print((np.sum(size)/1e9)/(down_end-down_start),'GB/s')
# outputting metadata to the csv.
links['size'] = size
links['output_path'] = outpath
links['download_executed'] = downloading
links['download_time'] = down_end-down_start
links['path_exists'] = links['output_path'].apply(check_link)
links['download_size (GB)'] = np.sum(size)/1e9
links['download_speed (GB)'] = (np.sum(size)/1e9)/(down_end-down_start)
if not os.path.exists('./logs/'+name.strip('.sh')):
    os.makedirs('./logs/'+name.strip('.sh'))
links.to_csv('./logs/'+name.strip('.sh')+'.csv')
