#!/bin/bash
#
# combine_images.sh
# execution script for combining processed individual spectral channels

## change home directory so CASA will run
HOME=$PWD

## unpack user arguments
file_suffix=$1
src_name=$2
output_name=$3
delta_nu=$4

output_name=${output_name}

## change working directory to staging area
mv combine_images.py /projects/vla-processing/images/${src_name}/single_field_imaging
cd /projects/vla-processing/images/${src_name}/single_field_imaging


# make casa call to imaging script
casa -c fitsconcat.py -f ${file_suffix} -o ${output_name} -d ${delta_nu}