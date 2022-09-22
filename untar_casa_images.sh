#!/bin/bash
#
# transfer_checksum.sh
# execution script to download checksum file for GASKAP-HI measurement set

cd tmp

## set source-specific parameters
source_name="WLM"
tarball_str="wlmctr_BCD_chan"
tarball_name="wlmctr_BCD_chan"$1".tar"

## copy tarball
cp /projects/vla-processing/images/$source_name/$tarball_name ./

## untar 
tar -xvf $tarball_name

## move to designated directory
mv *.image /projects/vla-processing/images/$source_name
mv *.image.pbcor /projects/vla-processing/images/$source_name
mv *.residual /projects/vla-processing/images/$source_name

## clean up
rm -rf $tarball_str*

