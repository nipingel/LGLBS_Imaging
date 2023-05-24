#!/bin/bash
#
# combine_images.sh
# execution script for combining processed individual spectral channels

## unpack user arguments
root_file_name=$1
file_suffix=$2
src_name=$3
chan=$4

## untar in node directory
tar -xvf /projects/vla-processing/images/${src_name}/${root_file_name}_chan${chan}_full.tar --directory .

## move untarred file back to staging area
mv *"."${file_suffix} /projects/vla-processing/images/${src_name}

## clean up 
rm -rf ${root_file_name}*