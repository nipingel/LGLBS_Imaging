#!/bin/bash
#
# split_channels.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set 

## TODO include ms_name and untar_name variables as argument into this executable script

## set up working directory
mv split_channels.py tmp
cd tmp
ls -ld /projects
ls -ld /projects/vla-processing
ls -ld /projects/vla-processing/measurement_sets
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD
## untar measurement set
## define untarred name
#ms_name="wlmctr_A+B+C+D_hi21cm.ms"
ms_name=$1

## untar measurement set to working directory
tar -xvf /projects/vla-processing/measurement_sets/WLM/$ms_name".tar" --directory .

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa -c split_channels.py -p $ms_name -s $2 -e $3

## tar measurement sets into files for each splitted-out channel
## arithmetic for loop
last_chan=$(($3-1))
for i in $( eval echo {$2..$last_chan})
do 
tar -cvf $ms_name"_chan"$i".tar" $ms_name"_chan"$i
done

mv $ms_name"_chan"*".tar" /projects/vla-processing/measurement_sets/WLM

## clean up
rm -rf $ms_name

