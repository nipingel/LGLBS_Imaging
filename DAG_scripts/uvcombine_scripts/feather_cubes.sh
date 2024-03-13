#!/bin/bash
#
# feather_cubes.sh
# execution script to feather two cubes together using uvcombine

## change home directory so CASA will run
HOME=$PWD

## define variables
sdcube=$1
interfcube=$2
outpath=$3
galaxy=$4
# full_path=/projects/vla-processing/measurement_sets/${src_name}

mkdir -p $outpath

# Direct to correct python environment
this_python=python

$this_python feather_cubes.py --sdcube ${sdcube} --interfcube ${interfcube} --outpath ${outpath} --galaxy ${galaxy}