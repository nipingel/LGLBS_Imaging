#!/bin/bash
#
# split_channels.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set 

## TODO include ms_name and untar_name variables as argument into this executable script

## set up working directory
mv ms_transform.py tmp
cd tmp

cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

## assign inputs & script variables
ms_name=$1
chan_width=$2
output_frame=$3
src_name=$4
untar_name=(${ms_name//.tar/ })
output_ms_name=$untar_name".transformed"

## untar measurement set to current working directory
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/raw_measurement_sets/${ms_name} --directory .

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile $output_ms_name".log" -c ms_transform.py -p ${untar_name} -w ${chan_width} -o ${output_ms_name} -f ${output_frame}

tar -cvf ${output_ms_name}".tar" ${output_ms_name}

mv ${output_ms_name}".tar" /projects/vla-processing/measurement_sets/${src_name}/raw_measurement_sets

## clean up
rm -rf ${untar_name}
