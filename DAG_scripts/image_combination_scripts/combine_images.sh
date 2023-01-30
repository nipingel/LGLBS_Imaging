#!/bin/bash
#
# combine_images.sh
# execution script for imaging of sub cube around absorption source

## untar CASA
mv combine_images.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

## untar measurement set
source_name="WLM"
suffix=$1
output_name=$2

## copy measurement set to working directory
cp -r /projects/vla-processing/images/$source_name/*"."$suffix ./

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa -c combine_images.py -f $suffix -o $output_name -d 1.954

mv $output_name* /projects/vla-processing/images/$source_name

## clean up
rm -rf $image_name*
