#!/bin/bash
#
# feather_cubes.sh
# execution script to feather two cubes together using uvcombine

## define variables
src_name=$1
sdcube=$2
interfcube=$3
outpath=$4
galaxy=$5

## download and install anaconda                                                                
wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh -O ~/anaconda.sh
bash ~/anaconda.sh -b -p $HOME/anaconda3
~/anaconda3/bin/conda clean -all -y


## create conda env for all astro tools
~/anaconda3/bin/conda create -c conda-forge -y -n astro_env astropy pip numpy scipy matplotlib
source ~/anaconda3/etc/profile.d/conda.sh
conda activate astro_env
pip install spectral_cube
pip install radio-beam
pip install reproject
tar -xvf uvcombine.tar --directory .


## change working directory to staging area
mv feather_cubes.py /projects/vla-processing/images/${src_name}
mv uvcombine /projects/vla-processing/images/${src_name}
cd /projects/vla-processing/images/${src_name}


~/anaconda3/bin/python feather_cubes.py --sdcube ${sdcube} --interfcube ${interfcube} --outpath ${outpath} --galaxy ${galaxy}