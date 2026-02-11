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
tar -xvf /projects/vla-processing/images/${src_name}/${root_file_name}_robust1.0_chan${chan}.tar --directory .

## extract sub-region
casa --nologfile --log2term --nogui -c imsub_image.py -n ${root_file_name}_robust1.0_chan${chan}.${file_suffix} -r M33_subregion.reg

## export to FITS
casa --nologfile --log2term --nogui -c export_fits.py -n ${root_file_name}_robust1.0_chan${chan}.${file_suffix}.imsub

## move untarred file back to staging area
mv ${root_file_name}_robust1.0_chan${chan}.${file_suffix}.imsub.fits /projects/vla-processing/images/${src_name}/${output_name}.fits

## clean up 
rm -rf ${root_file_name}*
