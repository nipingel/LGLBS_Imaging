#!/bin/bash
#
# uvcontsub_all.sh
# execution script to shift phase centre of ASKAP measurement sets to user specified value

## set up working directory
mv uvcontsub_indv.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar
tar -xzf ../packages.tar.gz --directory .
tar -xvf ../analysis_scripts.tar --directory .

HOME=$PWD

## define untarred name
tar_name=$1".transformed.tar"
untar_name=(${tar_name//.tar/ })

## untar measurement set to current working directory
tar -xvf /projects/vla-processing/measurement_sets/WLM/$tar_name --directory .

v_sys="-125"
v_width="210"
order="0"

## override system variables (**CHANGE THIS IN DOCKER FILE***)
export USER=ipython
export LOGNAME=ipython
# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile uvcontsub.log -c uvcontsub_indv.py -n $untar_name -o $order -v $v_sys -w $v_width

## pack up and copy back
tar -cvf $untar_name"_contsub.tar" $untar_name".contsub"
mv $untar_name"_contsub.tar" /projects/vla-processing/measurement_sets/WLM
rm -rf $untar_name
