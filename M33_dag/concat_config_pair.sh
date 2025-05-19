#!/bin/bash
#
# contcat_config_pair.sh
# execution script to concat measurement sets from configuration pair

tar -xvf analysis_scripts.tar

## change home directory so CASA will run
HOME=$PWD

## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH

## define variables
src_name=$1
config_pair=$2
output_name=$3
v_sys=$4
v_width=$5
full_path=/projects/vla-processing/measurement_sets/${src_name}/

## make call to casa
casa --nologfile -c concat_config_pair.py -p ${full_path} -o ${output_name} -a ${config_pair}

## make call to statwt
full_path=/projects/vla-processing/measurement_sets/${src_name}/${output_name}

## make copy of original
cp -r ${full_path} ${full_path}".orig"

## make call to casa
casa --nologfile -c statwt.py -n ${full_path} -v ${v_sys} -w ${v_width}

## append ".wt" suffix to denote that these measurement sets have been re-weighted
mv ${full_path} ${full_path}".wt"