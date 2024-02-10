#!/bin/bash
#
# image_channel.sh
# execution script for imaging single channel of LGLBS sources 

## change home directory so CASA will run
HOME=$PWD

tar -xvf analysis_scripts.tar
## set PYTHONPATH environment variable so statwt_bad_baseline.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH

## assign variables
ms_name=$1
src_name=$2
v_sys=$3
v_width=$4

## tar measurement set to working directory
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/${ms_name}".tar" --directory .

# make casa call to imaging script
/casa-6.5.0-15-py3.8/bin/casa --logfile reweight_casa_${ms_name}.log -c statwt.py -n ${ms_name} -v ${v_sys} -w ${v_width}

## append ".wt" suffix to denote that these measurement sets have been re-weighted
mv ${ms_name} ${ms_name}".wt"
mv ${ms_name}".wt" /projects/vla-processing/measurement_sets/${src_name}/${ms_name}".wt"