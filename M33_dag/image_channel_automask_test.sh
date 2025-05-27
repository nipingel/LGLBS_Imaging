#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## change home directory so CASA will run
HOME=$PWD

## assign variables
ms_name=$1
src_name=$2
ra_phase_center=$3
dec_phase_center=$4
ms_path=/projects/vla-processing/measurement_sets/${src_name}/clean_mask_test/${ms_name}
output_name=${ms_name}"_clean_automask"

# make casa call to imaging script
mpicasa -n 6 casa --logfile ${output_name}".log" -c image_channel_automask_test.py -v ${ms_path} -o ${output_name} -r ${ra_phase_center} -d${dec_phase_center}

## tar result
tar -cvf ${output_name}".tar" ${output_name}*
mv ${output_name}".tar" /projects/vla-processing/images/${src_name}/clean_mask_test/${output_name}".tar"