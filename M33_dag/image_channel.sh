#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## change home directory so CASA will run
HOME=$PWD

## assign variables
chan_num=$1
ms_name=$2"_chan"${chan_num}
src_name=$3
ra_phase_center=$4
dec_phase_center=$5
output_name=${ms_name}"robust1.0_chan"$1

## change directory
cd /projects/vla-processing/measurement_sets/${src_name}

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "$1" -lt "10" ]; then
       output_name=${ms_name}"robust1.0_chan00"$1
fi
if [ "$1" -lt "100" ] && [ "$1" -gt "9" ]; then
	output_name=${ms_name}"robust1.0_chan0"$1
fi

# make casa call to imaging script
casa --logfile ${output_name}".log" -c image_channel.py -v ${ms_name} -o ${output_name} -r ${ra_phase_center} -d${dec_phase_center}

## tar result
tar -cvf ${output_name}".tar" ${output_name}*

## clean up 
#rm -rf ${output_name}*