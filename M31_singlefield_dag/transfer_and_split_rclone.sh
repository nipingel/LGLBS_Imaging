#!/bin/bash
set -e

fname_full=$1
## strip filename of target/config prefix
fname=${fname_full#M31_B_}
src_name=$2
v_sys=$3 
v_width=$4 
rest_freq=$5 
time_bin_str=$6 
field1=$7
field2=$8

## unpack script tarballs
tar -xvf analysis_scripts.tar
tar -xvf phangs_imaging_scripts.tar
## change home directory so CASA will run
HOME=$PWD
## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH
export PYTHONPATH=./phangs_imaging_scripts:$PYTHONPATH

## rclone setup
rclone_base=/projects/vla-processing/measurement_sets/rclone-test
PATH=$PATH:$rclone_base/bin
conf=$rclone_base/config/rclone.conf

rclone sync lglbs:MeasurementSets/${fname_full}.tar ${HOME} --config ${conf}
touch ${fname_full}.done
tar -xvf ${fname_full}.tar
rm ${fname_full}.tar

## run casa script to split out the necessary fields
casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${fname} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field1}
casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${fname} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field2}

## tar and move to staging
tar -cvf ${fname}_spw.${field1}.tar ${fname}_spw.${field1}
tar -cvf ${fname}_spw.${field2}.tar ${fname}_spw.${field2}
mv ${fname}_spw*.tar /projects/vla-processing/measurement_sets/${src_name}/single-field-imaging
