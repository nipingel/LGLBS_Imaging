#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=50G
#SBATCH --array=0-423
#SBATCH --job-name=n6822-image-%A_%a
#SBATCH --output=logs/image_channel_%A_%a.out
#SBATCH --error=logs/image_channel_%A_%a.err
#SBATCH --mail-user=ekoch@ualberta.ca
#SBATCH --mail-type=FAIL
#
# image_channel.sh
# SLURM array replacement for image_channel.sub + image_channel.sh (HTCondor).
#
# Each array task runs tclean on a single spectral channel.  Output images
# are written directly to IMAGES_DIR on the shared filesystem.
#
# Key changes vs HTCondor version:
#   - No Docker container; uses module-loaded env + local CASA binary.
#   - No file transfer: channel MS is read from shared filesystem; tclean
#     output is written directly to IMAGES_DIR (no tar/untar cycle).
#   - Output file names are zero-padded to 4 digits at creation time,
#     so no separate untar_images renaming step is needed.
#
# The #SBATCH --array line is the default; submit_pipeline.sh overrides it
# with --array=0-$((N_IMAGING_CHANS-1)) from config.sh.
#
# To cap simultaneous tasks on a busy cluster, append %N to --array, e.g.:
#   sbatch --array=0-423%50 image_channel.sh

source "$(dirname "$0")/config.sh"

## ---------------------------------------------------------------------------
## Compute channel number and file paths for this array task
## ---------------------------------------------------------------------------

chan=$(( SLURM_ARRAY_TASK_ID + CHAN_START ))

# Zero-pad to 4 digits so files sort in channel order alphanumerically
if   [ "${chan}" -lt 10 ];   then padded="${chan}"; padded="000${chan}"
elif [ "${chan}" -lt 100 ];  then padded="00${chan}"
elif [ "${chan}" -lt 1000 ]; then padded="0${chan}"
else                              padded="${chan}"
fi

ms_chan_path="${INDV_CHAN_DIR}/${MS_NAME}_chan${chan}"
output_name="${IMAGES_DIR}/${MS_NAME}_chan${padded}_robust${ROBUST}"

echo "Array task ${SLURM_ARRAY_TASK_ID}: channel ${chan}"
echo "Input MS  : ${ms_chan_path}"
echo "Output    : ${output_name}"

## ---------------------------------------------------------------------------
## Environment
## ---------------------------------------------------------------------------

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load StdEnv
module load qt

source /home/ekoch/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/
export CASALD_LIBRARY_PATH=$LD_LIBRARY_PATH

python3 -c "import time, random; time.sleep(random.randint(2, 120))"

## ---------------------------------------------------------------------------
## Run CASA tclean
## ---------------------------------------------------------------------------

mkdir -p "${IMAGES_DIR}"

export script_args="-v ${ms_chan_path} -r ${RA_PHASE_CENTER} -d ${DEC_PHASE_CENTER} -o ${output_name}"
echo "Args passed to script: $script_args"
xvfb-run -a ${CASA_EXECUTABLE} --rcdir ~/.casa --nologger --nogui --log2term \
    -c ${SCRIPTS_DIR}/image_channel.py ${script_args}
