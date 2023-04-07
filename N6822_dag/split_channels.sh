#!/bin/bash
#
# split_channels.sh
# execution script to split out a range of channels from a staged and calibrated LGLBS measurement set for imaging

## set up working directory
mv split_channels.py tmp
cd tmp

## change home directory so CASA will run
HOME=$PWD

## assign variables
ms_name=$1
source_name=$2

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa -c split_channels.py -p ${ms_name} -s $3 -e $4 --indv_channel

## tar measurement sets into files for each splitted-out channel
## arithmetic for loop
last_chan=$(($3-1))
for i in $( eval echo {$2..$last_chan})
do 
tar -cvf ${ms_name}"_chan"$i".tar" ${ms_name}"_chan"$i
done


