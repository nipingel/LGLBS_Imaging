#!/bin/bash
#
# image_channel_config_pair.sh
# execution script for imaging a configuration pair in a single channel spectral channel


## change home directory so CASA will run
HOME=$PWD

$(ms_name) $(src_name) $(config_pair) $(ra_phase_center) $(dec_phase_center)

## assign variables
ms_name=$1
src_name=$2
config_pair=$3
ra_phase_center=$4
dec_phase_center=$5

ms_path=/projects/vla-processing/measurement_sets/${src_name}/config_pair_test/${ms_name}
output_name=${ms_name}"_config_pair_"${config_pair}"_chan"${chan_num}

# make mpicasa call to imaging script
mpicasa -n 6 casa --logfile ${output_name}".log" -c image_channel.py - -o ${output_name} -r ${ra_phase_center} -d${dec_phase_center}

## tar result
tar -cvf ${output_name}".tar" ${output_name}*
mv ${output_name}".tar" /projects/vla-processing/measurement_sets/${src_name}/config_pair_test/