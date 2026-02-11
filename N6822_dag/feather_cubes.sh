#!/bin/bash
#
# feather_cubes.sh
# execution script to feather two cubes together using uvcombine

## define variables
src_name=$1
sdcube=$2
interfcube=$3
outpath=$4
galaxy=$5

## change working directory to staging area
mv feather_cubes.py /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}
## set up python env
source /miniconda3/etc/profile.d/conda.sh
conda activate astro_env
HOME=$PWD

<<<<<<< HEAD
## change working directory to staging area
mv feather_cubes.py /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}

=======
## run feather
>>>>>>> m33-dag
python feather_cubes.py --sdcube ${sdcube} --interfcube ${interfcube} --outpath ${outpath} --galaxy ${galaxy}
