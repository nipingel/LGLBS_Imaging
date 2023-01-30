#!/bin/bash
#
# transfer_checksum.sh
# execution script to download checksum file for GASKAP-HI measurement set

cd tmp

## set source-specific parameters
source_name="WLM"
file_name=$1"_chan"$2
## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "$2" -lt "10" ]; then
        file_name=$1"_chan00"$2
fi
if [ "$2" -lt "100" ] && [ "$2" -gt "9" ]; then
        file_name=$1"_chan0"$2
fi

## untar 
tar -xvf /projects/vla-processing/images/$source_name/$file_name".tar" --directory .

## move to designated directory
mv *.image /projects/vla-processing/images/$source_name
mv *.image.pbcor /projects/vla-processing/images/$source_name
mv *.residual /projects/vla-processing/images/$source_name

## clean up
rm -rf $file_name*

