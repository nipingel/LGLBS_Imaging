#!/bin/bash
#
# statwt.sh
# execution script reweight visibilities based on rms in emission-free channels

tar -xvf analysis_scripts.tar

## change home directory so CASA will run
HOME=$PWD

## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH

##  set variables
ms_name=$1
v_sys=$2
v_width=$3
src_name=$4
full_path=/projects/vla-processing/measurement_sets/${src_name}/${ms_name}

## make call to casa
/casa-6.5.0-15-py3.8/bin/casa --nologfile -c statwt.py -n ${full_path} -v ${v_sys} -w ${v_width}

## append ".wt" suffix to denote that these measurement sets have been re-weighted
mv ${full_path} ${full_path}".wt"
