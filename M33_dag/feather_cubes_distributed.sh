#!/bin/bash
#
# feather_cubes.sh
# execution script to feather two cubes together using uvcombine

## define variables
src_name=$1
sdcube=$2
feathercube=$3
outpath=$4
galaxy=$5
start_chan=$6
end_chan=$7

## set up python env
source /miniconda3/etc/profile.d/conda.sh
conda activate astro_env

tar -xvf uvcombine.tar --directory /projects/vla-processing/images/${src_name}

## change working directory to staging area
mv feather_cubes_distributed.py /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}

echo $PATH
python feather_cubes_distributed.py --sdcube ${sdcube} --feathercube ${feathercube} --outpath ${outpath} --galaxy ${galaxy} --start_chan ${start_chan} --end_chan ${end_chan} 