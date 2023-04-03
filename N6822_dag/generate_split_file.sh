#!/bin/bash
#
# contcat_all.sh
# execution script to concat measurement sets from all measurement sets in staging area

mv generate_split_file.py tmp
cd tmp

src_name=$1
extension=$2
outfile_name=$3
path=/projects/vla-processing/measurement_sets/${src_name}

## change home directory so CASA will run
HOME=$PWD

## make call to casa
/casa-6.5.0-15-py3.8/bin/casa -c concat_all.py -p ${path} -o ${outfile_name} -e ${extension}

## how to move resulting text file to DAG directory?