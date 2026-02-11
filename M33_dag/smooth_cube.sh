#!/bin/bash
#
# feather_cubes.sh
# execution script to feather two cubes together using uvcombine

## define variables
src_name=$1
cube=$2
target_resolution=$3

## set up python env
source /miniconda3/etc/profile.d/conda.sh
conda activate astro_env

## change working directory to staging area
mv smooth_cube.py /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}

python smooth_cube.py -c ${cube} -t ${target_resolution} 