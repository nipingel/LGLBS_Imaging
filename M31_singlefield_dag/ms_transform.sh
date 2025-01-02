#!/bin/bash
#
# ms_trasform.sh
# execution script to place all split-out measurement sets on same spectral axis & reference frame  

## change home directory so CASA will run
HOME=$PWD

## assign inputs & script variables
ms_name=$1
chan_width=$2
output_frame=$3
src_name=$4
untar_name=(${ms_name//.tar/ })
output_ms_name=${untar_name}".transformed"

## copy measurement set to current working directory
cp -r /projects/vla-processing/measurement_sets/${src_name}/single-field-imaging/${ms_name} .

# make casa call to imaging script
casa --nologfile -c ms_transform.py -p ${untar_name} -w ${chan_width} -o ${output_ms_name} -f ${output_frame}

tar -cvf ${output_ms_name}".tar" ${output_ms_name}
mv ${output_ms_name}".tar" /projects/vla-processing/measurement_sets/${src_name}/single-field-imaging

## clean up
rm -rf ${untar_name}