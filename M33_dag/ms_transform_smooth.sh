#!/bin/bash
#
# ms_trasform.sh
# execution script to place all split-out measurement sets on same spectral axis & reference frame  

## change home directory so CASA will run
HOME=$PWD

## assign inputs & script variables
ms_name=$1
chan_width=$2
src_name=$3

## untar measurement set to current working directory
full_path=/projects/vla-processing/measurement_sets/${src_name}/${ms_name}
output_ms_name=${full_path}.${chan_width}kms.smoothed

# make casa call to imaging script
casa --nologfile -c ms_transform_smooth.py -p ${full_path} -w ${chan_width} -o ${output_ms_name}
