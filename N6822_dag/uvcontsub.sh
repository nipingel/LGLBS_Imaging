#!/bin/bash
#
# uvcontsub.sh
# execution script to subtract continuum from a LGLBS measurement set

tar -xvf analysis_scripts.tar --directory .

## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH

HOME=$PWD

## define script variables from input
ms_name=$1
v_sys=$2
v_width=$3
src_name=$4
untar_name=(${ms_name//.tar/ })
## untar
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/${ms_name} --directory .

# make casa call to uvcontsub script
/casa-6.5.0-15-py3.8/bin/casa --nologfile -c uvcontsub.py -n ${untar_name} -o 1 -v ${v_sys} -w ${v_width}

## move back to staging. DO NOT tar since files will be set up for concatenation in staging area next
mv $untar_name".contsub" /projects/vla-processing/measurement_sets/${src_name}
