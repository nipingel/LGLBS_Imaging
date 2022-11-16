#!/bin/bash
#
# transfer_checksum.sh
# execution script to download checksum file for GASKAP-HI measurement set

cd tmp

## set source-specific parameters
source_name="WLM"
file_name="wlmctr_ABCD_chan"$1

## untar 
tar -xvf /projects/vla-processing/images/$source_name/$file_name".tar" --directory .

## move to designated directory
mv *.image /projects/vla-processing/images/$source_name
mv *.image.pbcor /projects/vla-processing/images/$source_name
mv *.residual /projects/vla-processing/images/$source_name

## clean up
rm -rf $file_name*

