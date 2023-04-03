#!/bin/bash
#
# contcat_all.sh
# execution script to concat measurement sets from all measurement sets in staging area

mv combine_spw.sh tmp
cd tmp

src_name=$1
input_name=$2

## change home directory so CASA will run
HOME=$PWD


## make call to casa
/casa-6.5.0-15-py3.8/bin/casa -c combine_spw.py -s ${src_name} -n ${input_name}