#!/bin/bash

fname=$1
## activate globus environment
source /miniconda3/etc/profile.d/conda.sh
conda activate globus_env
HOME=$PWD

## set required environment variables
export GLOBUS_CLI_CLIENT_ID="6229281c-52b7-4d47-90a1-8dfb7a7a2852"
export GLOBUS_CLI_CLIENT_SECRET="Xct59EAStFcYlNr2KCaTmfGfhZD29DwHbEH2CRBcbGQ="

## globus setup
source_ep=08f85b7a-9541-4539-a332-5e7f0208b6b7
#dest_ep="33e45bdb-75ee-4ec0-b9a5-0f944565c2f6"
dest_ep=90443290-c363-4880-a17e-afebd4228278

## start transfer
echo "Beginning transfer of '${fname}'"

task_id=$(globus transfer "${source_ep}:M33/${fname}" "${dest_ep}:M33/${fname}" --jmespath 'task_id' --format=UNIX)

echo "Waiting on 'globus transfer' task '${task_id}'"
globus task wait ${task_id} --polling-interval 120
if [ $? -eq 0 ]; then
    echo "${task_id} completed successfully";
else
    echo "${task_id} failed!";
    # exit 1
fi

echo "Finished transferring at $(date)"

touch ${fname}.done
