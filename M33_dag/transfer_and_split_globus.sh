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

## set required environment variables
export GLOBUS_CLI_CLIENT_ID="6229281c-52b7-4d47-90a1-8dfb7a7a2852"
export GLOBUS_CLI_CLIENT_SECRET="Xct59EAStFcYlNr2KCaTmfGfhZD29DwHbEH2CRBcbGQ="

tar -xvf analysis_scripts.tar
tar -xvf phangs_imaging_scripts.tar
## change home directory so CASA will run
HOME=$PWD

## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH
export PYTHONPATH=./phangs_imaging_scripts:$PYTHONPATH

## globus setup
source_ep="08f85b7a-9541-4539-a332-5e7f0208b6b7"
dest_ep="33e45bdb-75ee-4ec0-b9a5-0f944565c2f6"


## start transfer
task_id=$(globus transfer ${source_ep}:${fname} ${dest_ep}:${fname} --jmespath 'task_id' --format=UNIX)

echo "Waiting on 'globus transfer' task '$task_id'"
globus task wait ${task_id} --polling-interval 120
if [ $? -eq 0 ]; then
    echo "${task_id} completed successfully";
else
    echo "${task_id} failed!";
    # exit 1
fi

echo "Finished transferring at $(date)"

touch ${fname}.done
tar -xvf ${fname}.tar
rm ${fname}.tar

## parse out the source name and config string after untarring
ms_name=${fname##*M31_B_}

## run casa script to split out the necessary fields
casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${ms_name} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field1}
casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${ms_name} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field2}

## tar and move to staging
tar -cvf ${ms_name}_spw.${field1}.tar ${ms_name}_spw.${field1}
tar -cvf ${ms_name}_spw.${field2}.tar ${ms_name}_spw.${field2}
mv ${ms_name}_spw* /projects/vla-processing/measurement_sets/M31/single-field-imaging