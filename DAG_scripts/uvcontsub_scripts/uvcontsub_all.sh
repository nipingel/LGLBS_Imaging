#!/bin/bash
#
# uvcontsub_all.sh
# execution script to shift phase centre of ASKAP measurement sets to user specified value

cd tmp

##  set measurement set nam, copy and untar
tar_name=$1".tar"
cp /projects/vla-processing/GASKAP-HI/measurement_sets/38814/phase_shifted/$tar_name .
tar -xvf $tar_name

chanRange=""
order=0

# make casa call to imaging script
casa-6.5.0-15-py3.8/bin/casa --logfile uvcontsub.log -c uvcontsub_indv.py -p $untar_name -c $order -l $chanRange

## pack up and copy back
tar -cvf $1"_contsub.tar" $1".contsub"
mv $1".contsub.tar" /projects/vla-processing/GASKAP-HI/measurement_sets/38814/contsub
rm $tar_name
