#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## untar CASA
mv image_channel.py tmp
cd tmp

## change home directory so CASA will run
HOME=$PWD

## untar measurement set
ms_name="NGC6822_A+B+C+D_combined_spw.ms_chan770"
source_name="NGC6822"

## copy measurement set to working directory
#tar -xvf /projects/vla-processing/measurement_sets/$source_name/$ms_name".tar" --directory .
cp -r /projects/vla-processing/measurement_sets/NGC6822/NGC6822_A+B+C+D_combined_spw.ms_chan770 .

output_name="NGC6822_A+B+C+D_combined_spw.ms_chan770_dirty"

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
#if [ "$3" -lt "10" ]; then
#        output_name=$2"_chan00"$3
#fi
#if [ "$3" -lt "100" ] && [ "$3" -gt "9" ]; then
#	output_name=$2"_chan0"$3
#fi

## added to continue a clean
#cp /projects/vla-processing/images/WLM/$output_name".tar" .
#tar -xvf $output_name".tar"

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa --logfile $output_name".log" -c image_channel.py -v $ms_name -o $output_name

## tar result
tar -cvf $output_name".tar" $output_name*

mv $output_name".tar" /projects/vla-processing/images/NGC6822

## clean up
rm -rf $ms_name
rm -rf $output_name*
