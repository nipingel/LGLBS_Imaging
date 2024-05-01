#!/bin/bash

fname=$1
src_name=$2
v_sys=$3 
v_width=$4 
rest_freq=$5 
time_bin_str=$6 
field1=$7
field2=$8

## activate globus environment
source /miniconda3/etc/profile.d/conda.sh
conda activate globus_env

tar -xvf analysis_scripts.tar
tar -xvf phangs_imaging_scripts.tar
## change home directory so CASA will run
HOME=$PWD

## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH
export PYTHONPATH=./phangs_imaging_scripts:$PYTHONPATH

## globus setup
source_ep=8dec4129-9ab4-451d-a45f-5b4b8471f7a3
dest_ep=e8fc98cc-9ca8-11eb-92cd-6b08dd67ff48
out_path=/projects/vla-processing/measurement_sets/{src_name}/single-field-imaging

## start transfer
task_id=$(globus transfer ${source_ep}:projects/rrg-eros-ab/ekoch/VLAXL/calibrated/${filename} ${dest_ep}:${out_path}/${filename} --jmespath 'task_id' --format=UNIX)
#task_id=$(globus transfer ${source_ep}:projects/rrg-eros-ab/ekoch/VLAXL/calibrated/archive/${filename} ${dest_ep}:${out_path}/${filename} --jmespath 'task_id' --format=UNIX)

touch ${fname}.done
tar -xvf ${fname}.tar
rm ${fname}.tar

## run casa script to split out the necessary fields
casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${fname} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field1}
casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${fname} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field2}

## get path to measurement set
ms_path = args.path

## tar and move to staging
tar -cvf ${fname}_spw.${field1}.tar ${fname}_spw.${field1}
tar -cvf ${fname}_spw.${field2}.tar ${fname}_spw.${field2}
mv ${fname}_spw* /projects/vla-processing/measurement_sets/M31/single-field-imaging