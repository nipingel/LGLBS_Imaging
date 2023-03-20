#!/bin/bash
#
# contcat_all.sh
# execution script reweight visibilities based on rms in emission-free channels

mv statwt.py tmp
mv analysis_scripts.tar tmp
cd tmp
tar -xvf analysis_scripts.tar
cp /scratch/casa-6.5.0-15-py3.8.tar.xz .
xz -d casa-6.5.0-15-py3.8.tar.xz
tar -xvf casa-6.5.0-15-py3.8.tar

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
tar -xvf /projects/vla-processing/measurement_sets/${src_name}/raw_measurement_sets/${ms_name} --directory .

## make call to casa
casa-6.5.0-15-py3.8/bin/casa -c statwt.py -n ${untar_name} -v ${v_sys} -w ${v_width}

## append ".wt" suffix to denote that these measurement sets have been re-weighted
mv ${untar_name} ${untar_name}".wt"

## pack up and copy back
tar -cvf ${untar_name}".wt.tar" ${untar_name}".wt"

mv ${untar_name}".wt.tar" /projects/vla-processing/measurement_sets/${src_name}/raw_measurement_sets
rm -rf ${untar_name}
rm -rf ${untar_name}".wt"

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
