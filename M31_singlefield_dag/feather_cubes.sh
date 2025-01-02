#!/bin/bash
#
# feather_cubes.sh
# execution script to feather two cubes together using uvcombine
## define variables
src_name=$1
sdcube=$2
field_name=$3
interfcube=$4
outpath=$5/${field_name}
galaxy=$6

## set up python env
source /miniconda3/etc/profile.d/conda.sh
conda activate astro_env

## change working directory to staging area
mv feather_cubes.py /projects/vla-processing/images/${src_name}/single-field-imaging/${field_name}
cd /projects/vla-processing/images/${src_name}/single-field-imaging/${field_name}

python feather_cubes.py --sdcube ${sdcube} --interfcube ${interfcube} --outpath ${outpath} --galaxy ${galaxy} --sdfactor 1.0