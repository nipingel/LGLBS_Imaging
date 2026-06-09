#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=100G
#SBATCH --job-name=n6822-feather-%J
#SBATCH --output=logs/feather_cubes_%J.out
#SBATCH --error=logs/feather_cubes_%J.err
#SBATCH --mail-user=ekoch@ualberta.ca
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#
# feather_cubes.sh
# SLURM replacement for feather_cubes.sub + feather_cubes.sh (HTCondor).
#
# Feathers the VLA interferometer cube with the GBT single-dish cube
# using uvcombine.feather_simple_cube via feather_cubes.py.
#
# Key changes vs HTCondor version:
#   - No Docker; activates an existing conda environment.
#   - Does NOT download or install Anaconda at job runtime.
#     A conda env with spectral_cube, radio_beam, reproject, and uvcombine
#     must already exist.  See README.md for setup.
#   - No file transfer; cubes and output live on shared filesystem.
#   - feather_cubes.py (this folder) has two bugs from N6822_dag fixed:
#       * duplicate '-f/--sdfactor' argparse argument removed
#       * 'scfactor' variable name typo fixed to 'sdfactor'

source "$(dirname "$0")/config.sh"

SD_CUBE_PATH="${IMAGES_DIR}/${SD_CUBE}"
INTERF_CUBE_PATH="${IMAGES_DIR}/${INTERF_CUBE}"
OUT_DIR="${IMAGES_DIR}"

echo "Interferometer cube : ${INTERF_CUBE_PATH}"
echo "Single-dish cube    : ${SD_CUBE_PATH}"
echo "Output directory    : ${OUT_DIR}"
echo "Galaxy              : ${FEATHER_GALAXY}"

## ---------------------------------------------------------------------------
## Environment
## ---------------------------------------------------------------------------

module load StdEnv

source /home/ekoch/.bashrc

# Activate the conda environment that has spectral_cube, uvcombine, etc.
if command -v conda &>/dev/null; then
    conda activate "${FEATHER_CONDA_ENV}"
else
    source "${HOME}/anaconda3/etc/profile.d/conda.sh"
    conda activate "${FEATHER_CONDA_ENV}"
fi

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

## ---------------------------------------------------------------------------
## Run feather_cubes.py
## ---------------------------------------------------------------------------

export script_args="-s ${SD_CUBE_PATH} -i ${INTERF_CUBE_PATH} -o ${OUT_DIR} -g ${FEATHER_GALAXY}"
echo "Args passed to script: $script_args"
python ${SCRIPTS_DIR}/feather_cubes.py ${script_args}
