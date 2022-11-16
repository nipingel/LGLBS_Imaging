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
ms_name="wlmctr_A+B+C+D_hi21cm.ms_chan"$1
source_name="WLM"

## copy measurement set to working directory
cp -r /projects/vla-processing/measurement_sets/$source_name/$ms_name ./

## define input values
output_name="wlmctr_ABCD_chan"$1

## added to continue a clean
#cp /projects/vla-processing/images/WLM/$output_name".tar" .
#tar -xvf $output_name".tar"

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile $output_name".log" -c image_WLM.py -v $ms_name -o $output_name

## tar result
tar -cvf $output_name".tar" $output_name*

mv $output_name".tar" /projects/vla-processing/images/$source_name

## clean up
rm -rf $ms_name
rm -rf $output_name*
