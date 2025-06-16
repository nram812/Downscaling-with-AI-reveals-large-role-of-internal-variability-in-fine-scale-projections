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
gcm="CMCC-ESM2"
variant="r1i1p1f1"
# the below is for CanESM5
#list=("r10i1p1f1"
#      "r10i1p2f1"
#      "r1i1p1f1"
#      "r1i1p2f1"
#      "r2i1p1f1"
#      "r2i1p2f1"
#      "r3i1p1f1"
#      "r3i1p2f1"
#      "r4i1p1f1"
#      "r4i1p2f1"
#      "r5i1p1f1"
#      "r5i1p2f1"DFD
#      "r6i1p1f1"
#      "r6i1p2f1"
#      "r7i1p1f1"
#      "r7i1p2f1"
#      "r8i1p1f1"
#      "r8i1p2f1"
#      "r9i1p1f1")
# these are for the ACCESS-ESM1-5 ensemble
#list=("r10i1p1f1"  "r13i1p1f1"  "r16i1p1f1"  "r19i1p1f1"  "r21i1p1f1"  "r24i1p1f1"  "r27i1p1f1"  "r2i1p1f1"   "r32i1p1f1"  "r35i1p1f1"  "r38i1p1f1"  "r40i1p1f1"  "r6i1p1f1"  "r9i1p1f1"
#"r11i1p1f1"  "r14i1p1f1"  "r17i1p1f1"  "r1i1p1f1"   "r22i1p1f1"  "r25i1p1f1"  "r28i1p1f1"  "r30i1p1f1"  "r33i1p1f1"  "r36i1p1f1"  "r39i1p1f1"  "r4i1p1f1"   "r7i1p1f1"
#"r12i1p1f1"  "r15i1p1f1"  "r18i1p1f1"  "r20i1p1f1"  "r23i1p1f1"  "r26i1p1f1"  "r29i1p1f1"  "r31i1p1f1"  "r34i1p1f1"  "r37i1p1f1"  "r3i1p1f1"   "r5i1p1f1"   "r8i1p1f1")
#list=("ssp126" "ssp245" "ssp370" "ssp585")
#list=("historical" "ssp126" "ssp245" "ssp370" "ssp585")
list=("ssp245")

for item in "${list[@]}"; do
  ssp="$item"
  echo "$gcm $variant $ssp"
  sbatch -J "${ssp}_${gcm}" run_slurm.sl $output_dir $variant $ssp $gcm
#  /home/rampaln/.conda/envs/bcsd/bin/python regrid_files.py $output_dir $variant $ssp $gcm
#  /home/rampaln/.conda/envs/bcsd/bin/python merge_files.py $output_dir $variant $ssp $gcm
#  /home/rampaln/.conda/envs/bcsd/bin/python merge_variables.py $output_dir $variant $ssp $gcm
#  /home/rampaln/.conda/envs/bcsd/bin/python delete_files.py $output_dir $variant $ssp $gcm
done


