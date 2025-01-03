#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## change home directory so CASA will run
HOME=$PWD

## assign variables
ms_name=$1
src_name=$2
ra_phase_center=$3
dec_phase_center=$4

## output name for precontub, no reweighting
##output_name=${ms_name}"_precontsub_noreweight"
## output name for precontsub, reweighting
##output_name=${ms_name}"_precontsub_reweight"
## output name for contsub, reweighting
##output_name=${ms_name}"_postcontsub_reweight"
## output name for pre-mstransform imaging
output_name=${ms_name}"_premstransform" 

## tar measurement set to working directory
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/${ms_name}".tar" --directory .
#cp -r /projects/vla-processing/measurement_sets/${src_name}/${ms_name} .

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa --logfile ${output_name}".log" -c image_bad_baseline_ms.py -v ${ms_name} -o ${output_name} -r ${ra_phase_center} -d${dec_phase_center}

## remove the original measurement set
rm -rf ${ms_name}

## tar result
tar -cvf ${output_name}".tar" ${output_name}*

mv ${output_name}".tar" /projects/vla-processing/images/${src_name}
## clean up 
rm -rf ${output_name}*
