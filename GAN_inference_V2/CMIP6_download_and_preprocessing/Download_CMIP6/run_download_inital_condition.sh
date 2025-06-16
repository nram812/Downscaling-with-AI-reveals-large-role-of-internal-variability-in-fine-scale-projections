#!/bin/bash -l



module use /opt/nesi/modulefiles/
module unuse /opt/niwa/CS500_centos7_skl/modules/all
module unuse /opt/niwa/share/modules/all

export SYSTEM_STRING=CS500
export OS_ARCH_STRING=centos7
export CPUARCH_STRING=skl
#export PYTHONNOUSERSITE=/home/rampaln/.local/lib/python3.9/site-packages
export PYTHONUSERBASE=/nesi/project/niwa00018/rampaln/conda_tmp
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/rampaln/.local/lib/python3.9/site-packages
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64
### Note add a separate log folder that Maxime has outlined
module purge # optional
module load NIWA
module load gcc/9.3.0
module load CDO/1.9.5-GCC-7.1.0
#module load Miniconda3/4.12.0
cd /nesi/nobackup/niwa00018/CMIP6_data/download-cmip6/WGETs
#CMIP6_FILE="CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3/CMIP6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3.ssp370.r1i1p1f1.day.hus.gr.sh"
CMIP6_FILE="ACCESS-ESM_sfc/"

for file in ${CMIP6_FILE}*; do
    # Check if the file exists (in case the pattern matches no files)
    if [[ -f "$file" ]]; then
        echo "Processing file: $file"

        # Check if "historical" is in the filename
        if [[ "$file" == *"historical"* ]]; then

            CMIP6_arg="historical"
            CMIP6_arg2="historical"
            sbatch /nesi/nobackup/niwa00018/CMIP6_data/download-cmip6/run_download_inital_condition.sl $file $CMIP6_arg $CMIP6_arg2
            echo "This is a historical file." $CMIP6_arg2 $CMIP6_arg
        fi

        if [[ "$file" == *"ssp370"* ]]; then
            #echo "This is a future file."
            CMIP6_arg="ssp370"
            CMIP6_arg2="ssp"
            echo "This is a FUTURE file." $CMIP6_arg2 $CMIP6_arg
            sbatch /nesi/nobackup/niwa00018/CMIP6_data/download-cmip6/run_download_inital_condition.sl $file $CMIP6_arg $CMIP6_arg2
        fi

        # Add additional processing commands here
    fi
done
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget_inital.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "hus" -w_ssp "historical" -n 10 -s "historical"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "ua" -w_ssp "ssp370" -n 10 -s "ssp"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "va" -w_ssp "ssp370" -n 10 -s "ssp"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "ta" -w_ssp "ssp370" -n 10 -s "ssp"
