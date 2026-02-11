#!/bin/bash
#
# generate_split_file.sh
# execution script to generate an input file for SPLIT CONCAT step

tar -xvf analysis_scripts.tar 
export PYTHONPATH=./analysis_scripts:$PYTHONPATH

src_name=$1
extension=$2
outfile_name=$3
path=/projects/vla-processing/measurement_sets/${src_name}

## change home directory so CASA will run
HOME=$PWD

## make call to casa
casa -c generate_split_file.py -p ${path} -o ${outfile_name} -e ${extension}