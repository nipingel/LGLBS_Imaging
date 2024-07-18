#!/bin/bash
#
# contcat_all.sh
# execution script to run ms_transform to combine spectral windows in a concatenated measurement set

## change home directory so CASA will run
HOME=$PWD

## assign inputs & script variables
input_name=$1
src_name=$2
full_path=/projects/vla-processing/measurement_sets/${src_name}/single-field-imaging

## make call to casa
casa --nologfile -c ms_transform_combine_spw.py -p ${full_path} -n ${input_name}