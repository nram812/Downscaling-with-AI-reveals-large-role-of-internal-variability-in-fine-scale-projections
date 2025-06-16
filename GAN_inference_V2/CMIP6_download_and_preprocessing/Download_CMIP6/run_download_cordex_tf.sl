#!/bin/bash -l
#SBATCH --job-name=predict_gpu
#SBATCH --nodes=1
#SBATCH --time=64:12:00
#SBATCH --mem=128G
#SBATCH --account=niwa00018
#SBATCH --partition=niwa_work
#SBATCH --cpus-per-task=20
#SBATCH --mail-user=neelesh.rampal@niwa.co.nz
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
#CMIP6_FILE="CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3/CMIP6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3.ssp370.r1i1p1f1.day.hus.gr.sh"
CMIP6_FILE="./CMIP6.CMIP.NCC.NorESM2.MM/CMIP6.ScenarioMIP.NCC.NorESM2-MM.ssp370.r1i1p1f1.day.zg.gn.sh"
# This could also be just historical etc.
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "va" -w_ssp "ssp245" -n 20 -s "ssp"
/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget_tf.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "zg" -w_ssp "historical" -n 10 -s "ssp"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "ua" -w_ssp "ssp370" -n 10 -s "ssp"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "va" -w_ssp "ssp370" -n 10 -s "ssp"
#/home/rampaln/.conda/envs/bcsd/bin/python generate_links_from_wget.py -o "/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/CMIP6_archive" -w $CMIP6_FILE -w_var "ta" -w_ssp "ssp370" -n 10 -s "ssp"
