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
#module load gcc/9.3.0
module load CDO/1.9.5-GCC-7.1.0
module load Miniforge3
cd /nesi/nobackup/niwa00018/morrishdg/CMIP_6_workflow/2_preprocess_ensembles


output_dir="/nesi/nobackup/niwa00018/CMIP6_data/OUTPUT/Downscaled_Preprocessed"
#ssp="ssp126"
gcm=("MPI-ESM1-2-HR" "ACCESS-CM2" "ACCESS-ESM1-5" "GISS-E2-1-G" "INM-CM4-8" "INM-CM5-0" "EC-Earth3" "TaiESM1" "IPSL-CM6A-LR" "MPI-ESM1-2-LR" "NorESM2-LM" "NorESM2-MM" "CanESM5" "UKESM1-0-LL" "IITM-ESM" "CMCC-ESM2" "EC-Earth3-Veg-LR" "CNRM-CM6-1" "EC-Earth3-Veg" "CMCC-CM2-SR5")
variant=("r1i1p1f1" "r4i1p1f1" "r1i1p1f1" "r1i1p1f2" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f2" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f2" "r1i1p1f1" "r1i1p1f1")
#gcm=("CMCC-ESM2" "EC-Earth3-Veg-LR" "CNRM-CM6-1")
#variant=("r1i1p1f1" "r1i1p1f1" "r1i1p1f2")


list=("historical" "ssp126" "ssp245" "ssp370" "ssp585")
for i in "${!gcm[@]}"; do
  echo "GCM: ${gcm[i]}, Variant: ${variant[i]}, jobname: ${ssp}_${gcm}"
  gcm="${gcm[i]}"
  variant="${variant[i]}"
  for item in "${list[@]}"; do
    ssp="$item"
    echo "$gcm $variant $ssp"
    sbatch -J "${ssp}_${gcm}" run_slurm_mass.sl $output_dir $variant $ssp $gcm
  #  /home/rampaln/.conda/envs/bcsd/bin/python regrid_files.py $output_dir $variant $ssp $gcm
  #  /home/rampaln/.conda/envs/bcsd/bin/python merge_files.py $output_dir $variant $ssp $gcm
  #  /home/rampaln/.conda/envs/bcsd/bin/python merge_variables.py $output_dir $variant $ssp $gcm
  #  /home/rampaln/.conda/envs/bcsd/bin/python delete_files.py $output_dir $variant $ssp $gcm
  done
done

