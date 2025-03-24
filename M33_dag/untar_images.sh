#!/bin/bash
#
# untar_images.sh
# execution script for untarring processed individual spectral channels

## unpack user arguments
file_suffix=$1
root_file_name=$2
src_name=$3
chan=$4
output_name=${root_file_name}_robust1.0_chan${chan}.${file_suffix}
## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "${chan}" -lt "10" ]; then
	output_name=${root_file_name}_robust1.0_chan000${chan}.${file_suffix}
fi
if [ "${chan}" -lt "100" ] && [ "${chan}" -gt "9" ]; then
	output_name=${root_file_name}_robust1.0_chan00${chan}.${file_suffix}
fi
if [ "${chan}" -lt "1000" ] && [ "${chan}" -gt "99" ]; then
        output_name=${root_file_name}_robust1.0_chan0${chan}.${file_suffix}
fi

## untar in node directory
#tar -xvf /projects/vla-processing/images/${src_name}/${root_file_name}_robust1.0_chan${chan}.tar --directory .

## move untarred file back to staging area
#mv ${root_file_name}_robust1.0_chan${chan}.${file_suffix} /projects/vla-processing/images/${src_name}/${output_name}

## clean up 
#rm -rf ${root_file_name}*

casa --nologfile --log2term --nogui -c export_fits.py -n /projects/vla-processing/images/${src_name}/${output_name} -e ${file_suffix}
