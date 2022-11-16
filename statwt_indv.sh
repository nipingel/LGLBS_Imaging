#!/bin/bash
#
# statwt_indv.sh
# execution script reweight visibilities based on rms in emission-free channels

mv statwt_indv.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

##  set measurement set name, copy and untar
## untar measurement set
ms_name=$1".transformed.contsub.tar"
untar_name=(${ms_name//.tar/ })
tar -xvf /projects/vla-processing/measurement_sets/WLM/$tar_name --directory .

## create copy
cp -r $untar_name $untar_name".wt"

## define velocity inputs
v_sys="-125"
v_width="210"

## make call to casa
casa-6.5.0-15-py3.8/bin/casa -c statwt_indv.py -p $untar_name".wt" -n $untar_name -v $v_sys -w $v_width

## pack up and copy back
tar -cvf $untar_name"wt.tar" $untar_name".wt"

mv $untar_name"wt.tar" /projects/vla-processing/measurement_sets/WLM
rm -rf $untar_name
rm -rf $untar_name".wt"
