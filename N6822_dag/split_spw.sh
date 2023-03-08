#!/bin/bash
#
# split_spw.sh
# execution script to split out spectral window from input LGLBS measurement set 

## set up working directory
mv split_spw.py tmp
mv analysis_scripts.tar tmp
mv phangs_imaging_scripts.tar tmp
cd tmp
tar -xvf analysis_scripts.tar
tar -xvf phangs_imaging_scripts.tar
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

export PYTHONPATH=./analysis_scripts:$PYTHONPATH
export PYTHONPATH=./phangs_imaging_scripts:$PYTHONPATH


## assign input variables
ms_name=$1
src_config=$2
v_sys=$3
v_width=$4
rest_freq=$5
src_name=$6

truncated_ms_name=(${ms_name//$src_config/ })
untar_name=(${truncated_ms_name//.tar/ })

## untar measurement set to current working directory
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/${ms_name} --directory .

# make casa call to split spw script
casa-6.5.0-15-py3.8/bin/casa --logfile split_spw.log -c split_spw.py -p ${untar_name} -v ${v_sys} -w ${v_width} -r ${rest_freq} -s ${src_name}

tar -cvf ${untar_name}"_spw.tar" ${untar_name}"_spw"

mv ${untar_name}"_spw.tar" /projects/vla-processing/measurement_sets/${src_name}

## clean up
rm -rf ${ms_name}
rm -rf ${untar_name}
