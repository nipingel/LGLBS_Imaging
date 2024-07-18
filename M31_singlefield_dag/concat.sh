#!/bin/bash
#
# contcat_all.sh
# execution script to concat measurement sets from all measurement sets in staging area

## change home directory so CASA will run
HOME=$PWD

## define variables
src_name=$1
full_path=/projects/vla-processing/measurement_sets/${src_name}/single-field-imaging

## make call to casa
casa --logfile concat.log -c concat_singlefield.py -p ${full_path}
