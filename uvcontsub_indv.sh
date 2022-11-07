#!/bin/bash
#
# uvcontsub_all.sh
# execution script to shift phase centre of ASKAP measurement sets to user specified value

cd tmp

tar -xzf ../packages.tar.gz -directory .
tar -xzf ../analysis_scripts.tar -directory .

HOME=$PWD

## untar measurement set to current working directory
tar -xvf /projects/vla-processing/measurement_sets/WLM/$ms_name --directory .
## define untarred name
tar_name=$1
untar_name=(${tar_name//.tar/ })

v_sys="-125"
v_width="210"
order="0"

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile uvcontsub.log -c uvcontsub_indv.py -p $untar_name -o $order -v $v_sys -w $v_width

## pack up and copy back
tar -cvf $untar_name"_contsub.tar" $untar_name".contsub"
mv $untar_name"_contsub.tar" /projects/vla-processing/measurement_sets/WLM
rm $untar_name
