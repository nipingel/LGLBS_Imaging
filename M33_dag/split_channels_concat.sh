#!/bin/bash
#
# split_channels_concat.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set
# to ensure all measurement sets have same number of channels for concat

## change home directory so CASA will run
HOME=$PWD

## assign variables
full_path=$1
start_chan=$2
end_chan=$3 

# make casa call to imaging script
casa --nologfile -c split_channels.py -p ${full_path} -s ${start_chan} -e ${end_chan} --split_concat