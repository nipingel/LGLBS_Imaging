#!/bin/bash
#
# split_channels_concat.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set
# to ensure all measurement sets have same number of channels for concat

## change home directory so CASA will run
HOME=$PWD

## assign variables
full_path=$1

# make casa call to imaging script
casa --nologfile -c split_channels.py -p ${full_path} -s $2 -e $3 --split_concat