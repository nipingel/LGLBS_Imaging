#!/bin/bash

src_name=$1
v_sys=$2
v_width=$3 
rest_freq=$4 
time_bin_str=$5 
field1=$6
field2=$7

## activate globus environment
source /miniconda3/etc/profile.d/conda.sh
conda activate globus_env

## set required environment variables
export GLOBUS_CLI_CLIENT_ID="6229281c-52b7-4d47-90a1-8dfb7a7a2852"
export GLOBUS_CLI_CLIENT_SECRET="Xct59EAStFcYlNr2KCaTmfGfhZD29DwHbEH2CRBcbGQ="

tar -xvf analysis_scripts.tar
tar -xvf phangs_imaging_scripts.tar

## copy to working directory
cp -r analysis_scripts /projects/vla-processing/measurement_sets/M31/single-field-imaging
cp -r phangs_imaging_scripts /projects/vla-processing/measurement_sets/M31/single-field-imaging
mv transfer_and_split.py /projects/vla-processing/measurement_sets/M31/single-field-imaging

## change home directory so CASA will run
HOME=$PWD

## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH
export PYTHONPATH=./phangs_imaging_scripts:$PYTHONPATH

## read from file list
FILENAMES=$(cat transfer-list_Bconfig_leftover.txt)

## change working directory
cd /projects/vla-processing/measurement_sets/M31/single-field-imaging

## globus setup
source_ep="08f85b7a-9541-4539-a332-5e7f0208b6b7"
dest_ep="33e45bdb-75ee-4ec0-b9a5-0f944565c2f6"
for fname in $FILENAMES; do
	## start transfer
	task_id=$(globus transfer ${source_ep}:${fname} ${dest_ep}:${fname} --jmespath 'task_id' --format=UNIX)
	echo "Waiting on 'globus transfer' task '$task_id'"
	globus task wait ${task_id} --polling-interval 120
	if [ $? -eq 0 ]; then
        	echo "$task_id completed successfully";
    	else
        	echo "$task_id failed!";
        	# exit 1
    	fi
    	echo "Finished transferring at $(date)"

	# Untar
	tar -xvf ${fname}
	rm ${fname}
	
	## parse out the source name and config string after untarring
	ms_name=${fname##*M31_B_}
	ms_name=${ms_name%.tar*}

	## run casa script to split out the necessary fields
	casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${ms_name} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field1}
	casa --nologfile --log2term --nogui -c transfer_and_split.py -p ${ms_name} -v ${v_sys} -w ${v_width} -r ${rest_freq} -t ${time_bin_str} -f ${field2}
done
