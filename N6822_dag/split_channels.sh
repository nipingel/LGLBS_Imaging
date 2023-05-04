#!/bin/bash
#
# split_channels.sh
# execution script to split out a range of channels from a staged and calibrated LGLBS measurement set for imaging

## change home directory so CASA will run
HOME=$PWD

## assign variables
ms_name=$1
source_name=$2
full_path="/projects/vla-processing/measurement_sets/"${source_name}"/"${ms_name}

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa --nologfile -c split_channels.py -p ${full_path} -s $3 -e $4 --indv_channel

## tar measurement sets into files for each splitted-out channel
cd /projects/vla-processing/measurement_sets/${source_name}/${ms_name}

## arithmetic for loop
last_chan=$(($4-1))
for i in $( eval echo {$3..$last_chan})
do 
	tar -cvf ${ms_name}"_chan"$i".tar" ${ms_name}"_chan"$i
done