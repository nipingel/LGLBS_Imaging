#!/bin/bash
#
# split_channels.sh
# execution script to split out range of channels from a staged and calibrated LGLBS measurement set 

## TODO include ms_name and untar_name variables as argument into this executable script

## set up working directory
mv split_spw.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

## assign input variables
ms_name=$1
src_config=$2
spw_str=$3
src_name=$4

truncated_ms_name=(${ms_name//$src_config/ })
untar_name=(${truncated_ms_name//.tar/ })

## untar measurement set to current working directory
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/${ms_name} --directory .

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile split_spw.log -c split_spw.py -p ${untar_name} -s ${spw_str}

tar -cvf ${untar_name}"_spw"${spw_str}".tar" ${untar_name}"_spw"${spw_str}

mv ${untar_name}"_spw"${spw_str}".tar" /projects/vla-processing/measurement_sets/${src_name}

## clean up
rm -rf ${ms_name}
rm -rf ${untar_name}
