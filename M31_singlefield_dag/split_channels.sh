#!/bin/bash
#
# split_channels.sh
# execution script to split out a range of channels from a staged and calibrated LGLBS measurement set for imaging

## change home directory so CASA will run
HOME=$PWD

## assign variables
ms_name_1="M31_field14.comb_spw.wt"
ms_name_2="M31_field47.comb_spw.wt"
source_name=$1
start_chan=$2
end_chan=$3
full_path_1=/projects/vla-processing/measurement_sets/${source_name}/single_field_imaging/${ms_name_1}
full_path_2=/projects/vla-processing/measurement_sets/${source_name}/single_field_imaging/${ms_name_2}

# make casa call to imaging script
casa --nologfile -c split_channels.py -p ${full_path_1} -s ${start_chan} -e ${end_chan} --indv_channel
casa --nologfile -c split_channels.py -p ${full_path_2} -s ${start_chan} -e ${end_chan} --indv_channel

## tar measurement sets into files for each splitted-out channel
cd /projects/vla-processing/measurement_sets/${source_name}/single_field_imaging

## arithmetic for loop
last_chan=$((${end_chan}-1))
for i in $( eval echo {${start_chan}..${last_chan})
do 
	tar -cvf ${ms_name_1}"_chan"$i".tar" ${ms_name_1}"_chan"$i
	tar -cvf ${ms_name_2}"_chan"$i".tar" ${ms_name_2}"_chan"$i
done