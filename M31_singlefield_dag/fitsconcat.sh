#!/bin/bash
#
# fitsconcat.sh
# execution script for combining processed individual spectral channels

## change home directory so CASA will run
HOME=$PWD

## unpack user arguments
file_suffix=$1
src_name=$2
output_name=$3
field_name=$4

## change working directory to staging area
full_path=/projects/vla-processing/images/${src_name}/single-field-imaging/${field_name}

casa -c fitsconcat.py -p ${full_path} -e ${file_suffix} -o ${output_name}
