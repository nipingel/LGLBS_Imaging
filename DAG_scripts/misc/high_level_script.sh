#!/bin/bash
#
## LGLBS_Imaging.sh
## high-level script to capture workflow of LGLBS Imaging pipeline/DAG. Note
## that the base directory on the CHTC system is assumed to be /projects/vla-processing

## first, run transfer.sub to pull from remote data repository
## arguments:
## - textfile with the names of files associated with a given source (spectral line); base directory in Google drive is: LGLBS/MeasurementSets
## output:
##	- tarball of measurement sets listed in the input textfile
condor_submit transfer.sub

## run split_channels.sub to split off the HI or OH spectral windows
## executable:
## - split_spw.sh (runs split_spw.py)
## arguments: 
## - textfile with the name of tarballed measurement sets
## - (in split_spw.sh for split_spw.py) string denoting spectral window to be split ('5' for HI line)
## - (in split_spw.sh for split_spw.py) path to input measurement set
## output:
## - tarball of measurement sets that have had spectral window split out with 'spw#' where # is the spectral window index appended to name
condor_submit split_spw.sub 

## place all split-out measurement sets on same spectral axis & reference frame
## executable:
## - ms_transform.sh (runs ms_transform.py)
## arguments:
## - textfile with names of tarballed & split out measurement sets
## - (in mstransform.sh for mstransform.py) output reference frame (e.g., 'LSRK' or 'BARY')
## - (in mstransform.sh for mstransform.py) channel width in units of Hz
## - (in mstransform.sh for mstransform.py) path to input measurement set
## - (in mstransform.sh for mstransform.py) name of output measurement set
## output:
## - tarball of measurement sets that have been transformed to the user provided reference frame and spectral channel width
condor_submit ms_tranform.sub

## re-weight visibilities based on root mean square noise in emission-free regions. Use systemic velocity and velocity width to mask channels with expected emission. 
## executable:
## - statwt_indv.sh (runs statwt_indv.py)
## arguments:
## - textfile with names of tarbelled, split-out, and transformed measurement sets
## - (in statwt_indv.sh for statwt_indv.py) systemic velocity of source
## - (in statwt_indv.sh for statwt_indv.py) velocity width of source
## - (in statwt_indv.sh for statwt_indv.py) path to input measurement set
## output:
## - tarball of re-weighted, transformed, and split-out measurement sets with '.wt' appended to tarball name
condor_submit statwt_all.sub

## subtract contribution from background sources. Use systemic velocity and velocity width to mask channels with expected emission. 
## executable:
## - uvcontsub_indv.sh (runs uvcontsub_indv.py)
## arguments:
## - textfile with names of tarballed, split-out, and transformed measurement sets
## - (in uvcontsub_indv.sh for uvcontsub_indv.py) path to input measurement set
## - (in uvcontsub_indv.sh for uvcontsub_indv.py) order of polynomial model
## - (in uvcontsub_indv.sh for uvcontsub_indv.py) velocity width of source
## - (in uvcontsub_indv.sh for uvcontsub_indv.py) systemic velocity of source
## output:
## - tarball of continuum-subtracted, re-weighted, transformed, and split-out measurement sets with '.contsub' appended to tarball name
condor_submit uvcontsub_all.sh

## concatenate (combine) measurement sets from all VLA configurations
## executable:
## - concat_all.sh (runs concat_all.py)
## arguments:
## - textfile with measurement set names group by VLA configuration
## - (in concat_all.sh for concat_all.py) list of measurement sets to be concatenated
## - (in concat_all.sh for concat_all.py) name of concatenated measurement set (combines VLA configuration A+B+C+D)
## output:
## - tarball of concatenated measurement set (combines VLA configurations A+B+C+D)
condor_submit concat_all.sub

## split out individual channels for imaging
## executable:
## - split_channels.sh (runs split_channels.py)
## arguments:
## - starting channel to begin splitting based on 'queue' number
## - ending channel to end splitting based on 'queue' number
## - (in split_channels.sh for split_channels.py) path to concatenated, continuum-subtracted, re-weighted, transformed, and split-out (spectral window) measurement sets 
## output:
## - (N_end - N_start) measurement sets of individual channels contained in concatenated measurement set
condor_submit split_channels

## run tclean (imaging algorithm). Note that specific imaging parameters are hardcoded into image_*.py script
## executable:
## - image_WLM.sh (runs image_WLM.py)
## arguments:
## - channel number (based on queue number OR from input list of specific channels)
## - (in image_WLM.sh for image_WLM.py) path to ipnut measurement set containing single channel
## - (in image_WLM.sh for image_WLM.py) name of prefix for output files
## - output:
## - tarball of the various 2D images of the source 
condor_submit imaging_submission.sub

## finally, combine the 2D images into 3-dimensional data cube (dims: sky position, sky position, frequency/velocity)
## executable:
## - combine_images.sh (runs combine_image.py)
## arguments:
## - (in combine_images.sh for combine_images.py) suffix (combine all files with *.residual, *.image, etc...)
## - (in combine_images.sh for combine_images.py) name of output data cube (in FITS format)
## - (in combine_images.sh for combine_images.py) spectral width of channels in kHz
## output:
## - final data cube
condor_submit combine_images.sub

## CLEAN UP???	
