#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --time=3:12:00
#SBATCH --mem=128G
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
#module load gcc/9.3.0
module load CDO/1.9.5-GCC-7.1.0
module load Miniforge3
cd /nesi/nobackup/niwa00018/morrishdg/CMIP_6_workflow/2_preprocess_ensembles

Job_name="${3}_${4}_${2}"


/home/rampaln/.conda/envs/bcsd/bin/python regrid_files.py $1 $2 $3 $4
/home/rampaln/.conda/envs/bcsd/bin/python merge_files.py $1 $2 $3 $4
/home/rampaln/.conda/envs/bcsd/bin/python merge_variables.py $1 $2 $3 $4
/home/rampaln/.conda/envs/bcsd/bin/python delete_files.py $1 $2 $3 $4
