#!/bin/bash
#
# statwt_indv.sh
# execution script reweight visibilities based on rms in emission-free channels

mv concat_all.py tmp
cd tmp
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

## change home directory so CASA will run
HOME=$PWD

##  set measurement set name, copy and untar
## untar measurement set
ms_names="wlmctr_A+B+C+D_hi21cm_0.ms wlmctr_A+B+C+D_hi21cm_1.ms wlmctr_A+B+C+D_hi21cm_2.ms wlmctr_B+C+D_hi21cm.ms.wt"

## copy and untar measurement sets
for s in $ms_names
do
	tar -xvf /projects/vla-processing/measurement_sets/WLM/$s".tar" --directory .
done

## define output_vis names
output_vis_name="wlmctr_A+B+C+D_hi21cm.ms"

## make call to casa
casa-6.5.0-15-py3.8/bin/casa -c concat_all.py -l $ms_names -o $output_vis_name

## pack up and copy back
tar -cvf $output_vis_name".tar" $output_vis_name

mv $output_vis_name".tar" /projects/vla-processing/measurement_sets/WLM

## clean up
for s in $ms_names
do 
	rm -rf $s
done
rm -rf $output_vis_name
