#!/bin/bash
#
# config.sh
# Shared configuration for the N6822 DAG-style SLURM imaging pipeline.
# Source this file at the top of every step script.
#
# Usage: source "$(dirname "$0")/config.sh"

## ---------------------------------------------------------------------------
## Source / observation parameters
## ---------------------------------------------------------------------------

export SRC_NAME="NGC6822"
export MS_NAME="NGC6822_A+B+C+D.comb_spw.wt"

export RA_PHASE_CENTER="19h44m57.74s"
export DEC_PHASE_CENTER="-14d48m12.4"

export ROBUST="1.0"

## ---------------------------------------------------------------------------
## Channel parameters
## ---------------------------------------------------------------------------

# Channel range to image (inclusive).  One SLURM array task per channel.
export CHAN_START=800
export CHAN_END=1223          # inclusive; 424 total
export N_IMAGING_CHANS=424   # = CHAN_END - CHAN_START + 1

# split_channels step: each array task splits SPLIT_CHUNK_SIZE consecutive
# channels so that all channels are available as individual MSes for imaging.
export SPLIT_CHAN_START=1000
export SPLIT_CHUNK_SIZE=5
export SPLIT_N_JOBS=50       # 50 tasks × 5 chans = channels 1000-1249

## ---------------------------------------------------------------------------
## Cube combination / feathering parameters
## ---------------------------------------------------------------------------

export DELTA_NU="1953.71094083"     # channel width in kHz (for FITS header)

export SD_CUBE="N6822_GBT_Jy.eq.nostokes.fits"
export INTERF_CUBE="NGC6822_A+B+C+D_HI_0p4kms.fits"
export FEATHER_GALAXY="ngc6822"

## ---------------------------------------------------------------------------
## Paths  (edit for your cluster layout)
## ---------------------------------------------------------------------------

export BASE_DIR="/home/ekoch/scratch/VLAXL_imaging"

# Directory containing the combined, statwt'd MS
export MS_DIR="${BASE_DIR}/imaging/ngc6822"

# Individual per-channel MSes are written to the same directory as the
# input MS (split_channels.py appends _chan{N} to the full MS path).
export INDV_CHAN_DIR="${MS_DIR}"

# tclean outputs and final cube go here
export IMAGES_DIR="${BASE_DIR}/images/${SRC_NAME}"

# Absolute path to this scripts directory (locates .py files at runtime)
export SCRIPTS_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# Log directory (created by submit_pipeline.sh before first submission)
export LOGS_DIR="${SCRIPTS_DIR}/logs"

## ---------------------------------------------------------------------------
## Software
## ---------------------------------------------------------------------------

export CASA_EXECUTABLE="/home/ekoch/casa-6.6.1-17-pipeline-2024.1.0.8/bin/casa"

# Conda environment with spectral_cube, uvcombine, etc. (feather step only)
export FEATHER_CONDA_ENV="astro_env"
