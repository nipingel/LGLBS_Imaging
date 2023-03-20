#!/bin/bash
#
# statwt.sh
# execution script reweight visibilities based on rms in emission-free channels

mv statwt.py tmp
mv analysis_scripts.tar tmp
cd tmp
tar -xvf analysis_scripts.tar

## change home directory so CASA will run
HOME=$PWD

## set PYTHONPATH environment variable so statwt.py can import analysis tools
export PYTHONPATH=./analysis_scripts:$PYTHONPATH

##  set measurement set name, copy and untar
## untar measurement set
ms_name=$1
v_sys=$2
v_width=$3
src_name=$4
untar_name=(${ms_name//.tar/ })
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/${ms_name} --directory .

## make call to casa
/casa-6.5.0-15-py3.8/bin/casa -c statwt.py -n ${untar_name} -v ${v_sys} -w ${v_width}

## append ".wt" suffix to denote that these measurement sets have been re-weighted
mv ${untar_name} ${untar_name}".wt"

## pack up and copy back
tar -cvf ${untar_name}".wt.tar" ${untar_name}".wt"

mv ${untar_name}".wt.tar" /projects/vla-processing/measurement_sets/${src_name}
rm -rf ${untar_name}
rm -rf ${untar_name}".wt"
