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
output_name=${ms_name}"_full"

## tar measurement set to working directory
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/indv_channels/${ms_name}".tar" --directory .

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "$1" -lt "10" ]; then
       output_name=${ms_name}"_chan00"$1
fi
if [ "$1" -lt "100" ] && [ "$1" -gt "9" ]; then
	output_name=${ms_name}"_chan0"$1
fi

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa --logfile ${output_name}".log" -c image_channel.py -v ${ms_name} -o ${output_name} -r ${ra_phase_center} -d${dec_phase_center}

## remove the original measurement set
rm -rf ${ms_name}

## tar result
tar -cvf ${output_name}".tar" ${output_name}*

mv ${output_name}".tar" /projects/vla-processing/images/${src_name}
## clean up 
rm -rf ${output_name}*
