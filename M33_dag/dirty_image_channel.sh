#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## change home directory so CASA will run
HOME=$PWD

## assign variables
chan_num=$1
ms_name=$2
src_name=$3
ra_phase_center=$4
dec_phase_center=$5
ms_path=/projects/vla-processing/measurement_sets/${src_name}/${ms_name}
output_name=${ms_name}"_dirty_robust1.0_chan"${chan_num}

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "$1" -lt "10" ]; then
       output_name=${ms_name}"_dirty_robust1.0_chan00"${chan_num}
fi
if [ "$1" -lt "100" ] && [ "$1" -gt "9" ]; then
	output_name=${ms_name}"_dirty_robust1.0_chan0"${chan_num}
fi

# make casa call to imaging script
casa --logfile ${output_name}".log" -c dirty_image_channel.py -v ${ms_path} -n ${chan_num} -o ${output_name} -r ${ra_phase_center} -d${dec_phase_center}

## tar result
tar -cvf ${output_name}".tar" ${output_name}*
mv ${output_name}".tar" /projects/vla-processing/images/${src_name}

## clean up 
rm -rf ${output_name}*