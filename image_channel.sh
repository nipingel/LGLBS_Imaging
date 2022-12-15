#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## untar CASA
mv image_channel.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

## untar measurement set
ms_name=$1"_chan"$3".tar"
source_name="WLM"

## copy measurement set to working directory
tar -xvf /projects/vla-processing/measurement_sets/$source_name/$ms_name --directory .

output_name=$2"_chan"$3

## added to continue a clean
#cp /projects/vla-processing/images/WLM/$output_name".tar" .
#tar -xvf $output_name".tar"

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile $output_name".log" -c image_channel.py -v $ms_name -o $output_name

## tar result
tar -cvf $output_name".tar" $output_name*

mv $output_name".tar" /projects/vla-processing/images/$source_name

## clean up
rm -rf $ms_name
rm -rf $output_name*
