#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=50G
#SBATCH --array=0-423
#SBATCH --job-name=n6822-restart-%A_%a
#SBATCH --output=logs/restart_image_%A_%a.out
#SBATCH --error=logs/restart_image_%A_%a.err
#SBATCH --mail-user=ekoch@ualberta.ca
#SBATCH --mail-type=FAIL
#
# restart_image_channel.sh
# SLURM array replacement for restart_image_channel.sub + restart_image_channel.sh.
#
# Resumes tclean from existing model/residual products (restart=True).
# Submit this instead of image_channel.sh when continuing a previous run.
#
# Unlike the HTCondor version, previous tclean products do not need to be
# untarred first: they are already present on the shared filesystem.

source "$(dirname "$0")/config.sh"

## ---------------------------------------------------------------------------
## Compute channel number and file paths
## ---------------------------------------------------------------------------

chan=$(( SLURM_ARRAY_TASK_ID + CHAN_START ))

if   [ "${chan}" -lt 10 ];   then padded="000${chan}"
elif [ "${chan}" -lt 100 ];  then padded="00${chan}"
elif [ "${chan}" -lt 1000 ]; then padded="0${chan}"
else                              padded="${chan}"
fi

ms_chan_path="${INDV_CHAN_DIR}/${MS_NAME}_chan${chan}"
output_name="${IMAGES_DIR}/${MS_NAME}_chan${padded}_robust${ROBUST}"

echo "Array task ${SLURM_ARRAY_TASK_ID}: restarting channel ${chan}"
echo "Input MS  : ${ms_chan_path}"
echo "Output    : ${output_name}  (must already exist)"

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
## Run CASA tclean (restart mode)
## ---------------------------------------------------------------------------

export script_args="-v ${ms_chan_path} -r ${RA_PHASE_CENTER} -d ${DEC_PHASE_CENTER} -o ${output_name}"
echo "Args passed to script: $script_args"
xvfb-run -a ${CASA_EXECUTABLE} --rcdir ~/.casa --nologger --nogui --log2term \
    -c ${SCRIPTS_DIR}/restart_image_channel.py ${script_args}
