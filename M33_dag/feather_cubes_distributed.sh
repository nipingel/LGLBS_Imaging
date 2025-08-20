#!/bin/bash
#
# feather_cubes.sh
# execution script to feather two cubes together using uvcombine

## define variables
src_name=$1
sdcube=$2
interfcube=$3
galaxy=$4
start_chan=$5
end_chan=$6

## set up python env
source /miniconda3/etc/profile.d/conda.sh
conda activate astro_env

## change working directory to staging area
#mv feather_cubes_distributed.py /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}

echo $PATH
python feather_cubes_distributed.py --sdcube ${sdcube} --interfcube ${interfcube} --galaxy ${galaxy} --beginning_channel ${start_chan} --last_channel ${end_chan}
