#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## change home directory so CASA will run
HOME=$PWD

## assign variables
chan_num=$1
src_name=$2
ms_name_1="/projects/vla-processing/measurement_sets/"${src_name}"/single-field-imaging/M31_field14.comb_spw.wt"
ms_name_2="/projects/vla-processing/measurement_sets/"${src_name}"/single-field-imaging/M31_field47.comb_spw.wt"
ra_phase_center_1="00h41m29.752s"
dec_phase_center_1="41d26m40.64200"
ra_phase_center_2="00h48m42.535000s"
dec_phase_center_2="42d00m51.1220"

output_name_1="M31_field14.comb_spw.wt_chan"${chan_num}
output_name_2="M31_field47.comb_spw.wt_chan"${chan_num}

## tar measurement set to working directory
## tar -xvf /projects/vla-processing/measurement_sets/${src_name}/single_field_imaging/${ms_name_1}".tar" --directory .
## tar -xvf /projects/vla-processing/measurement_sets/${src_name}/single_field_imaging/${ms_name_2}".tar" --directory .

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "$1" -lt "10" ]; then
	output_name_1="M31_field14.comb_spw.wt_chan00"${chan_num}
       output_name_2="M31_field47.comb_spw.wt_chan00"${chan_num}
fi
if [ "$1" -lt "100" ] && [ "$1" -gt "9" ]; then
	output_name_1="M31_field14.comb_spw.wt_chan0"${chan_num}
	output_name_2="M31_field47.comb_spw.wt_chan0"${chan_num}
fi

# make casa call to imaging script
casa --logfile ${output_name}".log" -c image_channel.py -v ${ms_name_1} -n ${chan_num} -o ${output_name_1} -r ${ra_phase_center_1} -d${dec_phase_center_1}
casa --logfile ${output_name}".log" -c image_channel.py -v ${ms_name_2} -n ${chan_num} -o ${output_name_2} -r ${ra_phase_center_2} -d${dec_phase_center_2}


## remove the original measurement set
## rm -rf ${ms_name_1}
## rm -rf ${ms_name_2}

## tar result
tar -cvf ${output_name_1}".tar" ${output_name_1}*
tar -cvf ${output_name_2}".tar" ${output_name_2}*

mv ${output_name_1}".tar" /projects/vla-processing/images/${src_name}/single-field-imaging/M31_field14
mv ${output_name_2}".tar" /projects/vla-processing/images/${src_name}/single-field-imaging/M31_field47
## clean up 
rm -rf ${output_name_1}*
rm -rf ${output_name_2}*
