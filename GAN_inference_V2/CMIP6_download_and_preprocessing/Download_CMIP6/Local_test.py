import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import requests
from multiprocessing.dummy import Pool as ThreadPool
import urllib
import pathlib
import os, sys, threading
sys.path.append(r'./get-data')
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
import logging
import argparse
parser = argparse.ArgumentParser(description='Download CMIP6 Data')

variables=['ta']
ssps = 'historical'
output_path = '/Users/lewisho/Downloads'
name = 'CMIP6.CMIP.NCAR.CESM2-WACCM.historical.r1i1p1f1.day.hus.gn.sh'
wget_var = 'hus'
ssp = 'historical'
threads = 2
path = '/Users/lewisho/Desktop/'

from file_downloader import FileDownloader
from scrape_links import *
links = Scrape_WGET(path+name,wget_var,ssp, startdate=1950, enddate=2100,
                variables =variables, ssps=ssps)
links = pd.melt(links, id_vars =['variables','ssps'])
links = links.swifter.apply(lambda a: [i.strip("'") for i in a])
print(links.value)

# =============================================================================
# down_start = time.time()
# print('1')
# downloader = FileDownloader(max_threads=int(threads))
# # download the files
# print('2')
# outpath, size, downloading = download_list(downloader, links, output_path)
# print('3')
# down_end = time.time()
# print('Download Time:',down_end-down_start)
# print('Downloaded:',len(size),'Files, with a size of:',np.sum(size)/1e9,'GB')
# print((np.sum(size)/1e9)/(down_end-down_start),'GB/s')
# # outputting metadata to the csv.
# links['size'] = size
# links['output_path'] = outpath
# links['download_executed'] = downloading
# links['download_time'] = down_end-down_start
# links['path_exists'] = links['output_path'].apply(check_link)
# links['download_size (GB)'] = np.sum(size)/1e9
# links['download_speed (GB)'] = (np.sum(size)/1e9)/(down_end-down_start)
# if not os.path.exists('./logs/'+name.strip('.sh')):
#     os.makedirs('./logs/'+name.strip('.sh'))
# links.to_csv('./logs/'+name.strip('.sh')+'.csv')
# 
# =============================================================================

