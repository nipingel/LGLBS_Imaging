#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## change home directory so CASA will run
HOME=$PWD

## assign variables
chan_num=$1
root_file_name=$2
src_name=$3
ra_phase_center=$4
dec_phase_center=$5

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
#if [ "$1" -lt "10" ]; then
#       output_name=${ms_name}"_robust1.0_chan00"${chan_num}
#fi
#if [ "$1" -lt "100" ] && [ "$1" -gt "9" ]; then
#	output_name=${ms_name}"_robust1.0_chan0"${chan_num}
#fi

cp image_channel_restart.py /projects/vla-processing/images/${src_name}/restart_test
cd /projects/vla-processing/images/${src_name}/restart_test

# make mpicasa call to imaging script
mpicasa -n 6 casa --logfile ${output_name}".log" -c image_channel_restart.py -v M33_A+B+C+D_chan830.ms -o M33_A+B+C+D.ms_robust1.0_chan830 -r ${ra_phase_center} -d${dec_phase_center}

## tar result
#tar -cvf ${output_name}".tar" ${output_name}*
#mv ${output_name}".tar" /projects/vla-processing/images/${src_name}/restart_test

## clean up 
#rm -rf ${output_name}*
