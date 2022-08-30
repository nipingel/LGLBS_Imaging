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
ms_name="wlmctr_B+C+D_hi21cm.ms.tar"
untar_name="imaging/wlmctr/wlmctr_B+C+D_hi21cm.ms"

## copy measurement set to working directory
cp /projects/vla-processing/measurement_sets/WLM/$ms_name ./

## untar 
tar -xvf $ms_name

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile split_chans_$1_to_$2.log -c split_channels.py -p $untar_name -s $1 -e $2

#tar -cvf split_chans_$1_to_$2.tar *_chan* *.log

mv *_chan* /projects/vla-processing/measurement_sets/WLM
mv imaging/wlmctr/*_chan* /projects/vla-processing/measurement_sets/WLM

## clean up
rm -rf $ms_name
rm -rf $untar_name

