#!/bin/bash
#
# split_channels_concat.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set
# to ensure all measurement sets have same number of channels for concat

## set up working directory
mv split_channels.py tmp
cd tmp

## change home directory so CASA will run
HOME=$PWD

## assign variables
ms_name=$1
source_name=$2

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa -c split_channels.py -p $ms_name -s $3 -e $4 --split_concat

