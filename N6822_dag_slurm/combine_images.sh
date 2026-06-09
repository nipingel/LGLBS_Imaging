#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=75G
#SBATCH --job-name=n6822-combine-%J
#SBATCH --output=logs/combine_images_%J.out
#SBATCH --error=logs/combine_images_%J.err
#SBATCH --mail-user=ekoch@ualberta.ca
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#
# combine_images.sh
# SLURM replacement for combine_images.sub + combine_images.sh (HTCondor).
#
# Assembles individual per-channel 2D images into a 3D FITS cube using
# CASA (ia.imageconcat, imsmooth, exportfits).
#
# Key changes vs HTCondor version:
#   - No Docker; uses module-loaded env + local CASA binary.
#   - No file transfer; images are already on the shared filesystem.
#   - combine_images.py uses glob.glob('*.image') relative to CWD;
#     we cd to IMAGES_DIR so the glob finds all channel images.
#     HTCondor achieved the same by copying the script into the images dir;
#     here we keep the script in SCRIPTS_DIR and only change CWD.

source "$(dirname "$0")/config.sh"

echo "Combining images in : ${IMAGES_DIR}"
echo "File suffix         : image"
echo "Output name         : ${SRC_NAME}_ABCD"
echo "Delta nu            : ${DELTA_NU} kHz"

## ---------------------------------------------------------------------------
## Environment
## ---------------------------------------------------------------------------

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load StdEnv
module load qt

source /home/ekoch/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/
export CASALD_LIBRARY_PATH=$LD_LIBRARY_PATH

## ---------------------------------------------------------------------------
## cd to images dir so combine_images.py glob finds the per-channel images,
## then run CASA with an absolute path to the script.
## ---------------------------------------------------------------------------

cd "${IMAGES_DIR}"

export script_args="-f image -o ${SRC_NAME}_ABCD -d ${DELTA_NU}"
echo "Args passed to script: $script_args"
xvfb-run -a ${CASA_EXECUTABLE} --rcdir ~/.casa --nologger --nogui --log2term \
    -c ${SCRIPTS_DIR}/combine_images.py ${script_args}
