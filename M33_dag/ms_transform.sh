#!/bin/bash
#
# ms_trasform.sh
# execution script to place all split-out measurement sets on same spectral axis & reference frame  

## change home directory so CASA will run
HOME=$PWD

## assign inputs & script variables
ms_name=$1
chan_width=$2
output_frame=$3
src_name=$4
restfreq=$5

## untar measurement set to current working directory
cp -r /projects/vla-processing/measurement_sets/${src_name}/${ms_name} .
output_ms_name=${ms_name}".transformed"

# make casa call to imaging script
casa --nologfile -c ms_transform.py -p ${ms_name} -w ${chan_width} -o ${output_ms_name} -f ${output_frame} -r ${restfreq}

mv ${output_ms_name} /projects/vla-processing/measurement_sets/${src_name}

## clean up
rm -rf ${ms_name}