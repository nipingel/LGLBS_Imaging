#!/bin/bash
#
# image_WLM.sh
# execution script for imaging of sub cube around absorption source

## untar CASA
mv image_WLM.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

## untar measurement set
ms_name="wlmctr_B+C+D_hi21cm.ms_chan"$1

## copy measurement set to working directory
cp -r /projects/vla-processing/measurement_sets/$ms_name ./

## define input values
output_name="wlmctr_BCD_chan"$1

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile wlmctr_BCD_chan$1.log -c image_WLM.py -v $ms_name -o $output_name

mv $output_name* /projects/vla-processing/images/WLM

## clean up
rm -rf $ms_name
