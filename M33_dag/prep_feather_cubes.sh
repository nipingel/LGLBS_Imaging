#!/bin/bash
#
# prep_feather_cubes.sh
# execution script to prepare feathered data products 

## define variables
src_name=$1
sdcube=$2
interfcube=$3
feathercube=$4

## set up python env
source /miniconda3/etc/profile.d/conda.sh
conda activate astro_env

## change working directory to staging area
mv prep_feather_cubes.py /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}

echo $PATH
python prep_feather_cubes.py --sdcube ${sdcube} --interfcube ${interfcube} --feathercube ${feathercube} 
