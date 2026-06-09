#!/bin/bash
#SBATCH --time=4:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --array=0-49
#SBATCH --job-name=n6822-split-%A_%a
#SBATCH --output=logs/split_channels_%A_%a.out
#SBATCH --error=logs/split_channels_%A_%a.err
#SBATCH --mail-user=ekoch@ualberta.ca
#SBATCH --mail-type=FAIL
#
# split_channels.sh
# SLURM array replacement for split_channels.sub + split_channels.sh (HTCondor).
#
# Each array task splits SPLIT_CHUNK_SIZE consecutive channels from the
# combined, statwt'd measurement set into individual per-channel MSes.
# Output MSes are written directly to the shared filesystem (no tarball).
#
# HTCondor equivalent used Docker; this script uses module-loaded env + CASA.
# HTCondor used file staging (tarballs); here CASA reads/writes shared scratch.
#
# The #SBATCH --array line is the default; submit_pipeline.sh overrides it
# with --array=0-$((SPLIT_N_JOBS-1)) computed from config.sh.

source "$(dirname "$0")/config.sh"

## ---------------------------------------------------------------------------
## Compute channel range for this array task
## ---------------------------------------------------------------------------

start_chan=$(( SLURM_ARRAY_TASK_ID * SPLIT_CHUNK_SIZE + SPLIT_CHAN_START ))
end_chan=$(( start_chan + SPLIT_CHUNK_SIZE ))   # exclusive upper bound for CASA

echo "Array task ${SLURM_ARRAY_TASK_ID}: splitting channels ${start_chan} to $((end_chan - 1))"
echo "Input MS : ${MS_DIR}/${MS_NAME}"

## ---------------------------------------------------------------------------
## Environment  (mirrors fir_imaging/job_submit_lglbs_HI_imaging.sh)
## ---------------------------------------------------------------------------

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load StdEnv
module load qt

source /home/ekoch/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/
export CASALD_LIBRARY_PATH=$LD_LIBRARY_PATH

# Stagger start times to avoid simultaneous filesystem hits
python3 -c "import time, random; time.sleep(random.randint(2, 120))"

## ---------------------------------------------------------------------------
## Make output directory and run CASA split
## ---------------------------------------------------------------------------

mkdir -p "${INDV_CHAN_DIR}"

export script_args="-p ${MS_DIR}/${MS_NAME} -s ${start_chan} -e ${end_chan} --indv_channel"
echo "Args passed to script: $script_args"
xvfb-run -a ${CASA_EXECUTABLE} --rcdir ~/.casa --nologger --nogui --log2term \
    -c ${SCRIPTS_DIR}/split_channels.py ${script_args}
