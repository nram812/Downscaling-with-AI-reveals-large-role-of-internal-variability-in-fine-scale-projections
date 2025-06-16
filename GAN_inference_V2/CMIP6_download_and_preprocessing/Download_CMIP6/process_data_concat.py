import xarray as xr
import glob
from dask.diagnostics import ProgressBar
from dask import delayed, compute





def load_files(variable, ssp ='ssp370'):
    files = glob.glob(
        fr'//nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM/{variable}/6hrPlevPt/{ssp}/*.nc')
    with ProgressBar():
        df = xr.open_mfdataset(files, parallel=True, chunks={"time":1000})
        df = df.sel(lat=slice(-55, -20), lon=slice(150, 200), plev=[8.5e4, 5e4])
        #with ProgressBar():
        df.to_netcdf(fr'/nesi/project/niwa00018/ML_downscaling_CCAM/output/NorESM2-MM/process_data/NorESM2-MM_cm2_{ssp}_{variable}.nc')

tasks = []
for variable in ['hus']:
    load_files(variable)
