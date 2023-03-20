#!/bin/bash
#
# contcat_all.sh
# execution script to concat measurement sets from all measurement sets in staging area

mv concat_all.py tmp
cd tmp

src_name=$1
outfile_name=$2

## change home directory so CASA will run
HOME=$PWD

## make call to casa
/casa-6.5.0-15-py3.8/bin/casa -c concat_all.py -s ${src_name} -o ${outfile_name}