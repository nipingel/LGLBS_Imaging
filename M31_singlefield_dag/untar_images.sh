#!/bin/bash
#
# untar_images.sh
# execution script for untarring processed individual spectral channels

## unpack user arguments
file_suffix=$1
src_name=$2
chan=$3
root_file_name_1=$4
root_file_name_2=$5

output_name_1=${root_file_name_1}_chan${chan}.${file_suffix}
output_name_2=${root_file_name_2}_chan${chan}.${file_suffix}

## check if 0 needs to be appended in name (channel range from 0 to 99) for alphanumeric ordering
if [ "${chan}" -lt "10" ]; then
	output_name_1=${root_file_name_1}_chan000${chan}.${file_suffix}
	output_name_2=${root_file_name_2}_chan000${chan}.${file_suffix}
fi
if [ "${chan}" -lt "100" ] && [ "${chan}" -gt "9" ]; then
	output_name_1=${root_file_name_1}_chan00${chan}.${file_suffix}
	output_name_2=${root_file_name_2}_chan00${chan}.${file_suffix}
fi
if [ "${chan}" -lt "1000" ] && [ "${chan}" -gt "99" ]; then
        output_name_1=${root_file_name_1}_chan0${chan}.${file_suffix}
        output_name_2=${root_file_name_2}_chan0${chan}.${file_suffix}
fi

## untar in node directory
tar -xvf /projects/vla-processing/images/${src_name}/single_field_imaging/${root_file_name_1}_chan${chan}.tar --directory .
tar -xvf /projects/vla-processing/images/${src_name}/single_field_imaging/${root_file_name_2}_chan${chan}.tar --directory .

## move untarred file back to staging area
mv ${root_file_name_1}_chan${chan}.${file_suffix} /projects/vla-processing/images/${src_name}/single_field_imaging/${output_name_1}
mv ${root_file_name_2}_chan${chan}.${file_suffix} /projects/vla-processing/images/${src_name}/single_field_imaging/${output_name_2}

## clean up 
rm -rf ${root_file_name_1}*
rm -rf ${root_file_name_2}*