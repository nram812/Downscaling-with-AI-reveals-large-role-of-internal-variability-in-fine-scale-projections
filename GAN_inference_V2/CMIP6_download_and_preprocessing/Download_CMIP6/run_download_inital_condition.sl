#!/bin/bash -l
#SBATCH --job-name=predict_gpu
#SBATCH --nodes=1
#SBATCH --time=64:12:00
#SBATCH --mem=64G
#SBATCH --account=niwa00018
#SBATCH --partition=niwa_work
#SBATCH --cpus-per-task=10
#SBATCH --mail-type=ALL
#SBATCH --output log/%j-%x.out
#SBATCH --error log/%j-%x.out


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
cd /nesi/nobackup/niwa00018/CMIP6_data/download-cmip6
#CMIP6_FILE="CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3/CMIP6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3.ssp370.r1i1p1f1.day.hus.gr.sh"
#CMIP6_FILE="initial_condition_EC/CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3.historical.r6i1p1f1.day.hus.gr.sh"
/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget_inital.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $1 -w_var "pr" -w_ssp $2 -n 10 -s $3
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget_inital.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $1 -w_var "hus" -w_ssp $2 -n 10 -s $3
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "ua" -w_ssp "ssp370" -n 10 -s "ssp"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "va" -w_ssp "ssp370" -n 10 -s "ssp"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "ta" -w_ssp "ssp370" -n 10 -s "ssp"
