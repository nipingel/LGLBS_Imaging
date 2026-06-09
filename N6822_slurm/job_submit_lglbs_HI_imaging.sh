#!/bin/bash
#SBATCH --time=100:00:00
#SBATCH --cpus-per-task=64
#SBATCH --mem=256G
#SBATCH --array=1-22
#SBATCH --job-name=lglbs-hi-imaging-%A-%a
#SBATCH --output=lglbs-hi-imaging-%A-%a.out
#SBATCH --mail-user=ekoch@ualberta.ca
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# NGC6822 chunked HI imaging job.
#
# Mirrors fir_imaging/job_submit_lglbs_HI_imaging.sh exactly, with
# N6822-specific defaults.  Arguments can be overridden at submission:
#
#   sbatch job_submit_lglbs_HI_imaging.sh [galaxy] [line_product] [config] [chunksize]
#
# Defaults:  ngc6822  hi21cm  A+B+C+D  20
#
# The #SBATCH --array range sets the number of chunks.  For ngc6822 hi21cm
# with chunksize=20, nchunks ≈ 22.  Override via submit_pipeline.sh or by
# passing --array=1-N to sbatch directly.
#
# ImagingChunkedHandler will skip gracefully if SLURM_ARRAY_TASK_ID
# exceeds the actual nchunks, so it is safe to set the array slightly
# larger than needed.

export this_galaxy=${1:-ngc6822}
export this_line_product=${2:-hi21cm}
export this_config=${3:-A+B+C+D}
export this_chunksize=${4:-20}
export this_idx=${SLURM_ARRAY_TASK_ID}

echo $SLURM_CPUS_PER_TASK

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load StdEnv
module load qt

source /home/ekoch/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/

export CASALD_LIBRARY_PATH=$LD_LIBRARY_PATH


# Ensure no time overlap in job start times
python3 -c "import time, random; time.sleep(random.randint(2, 120))"

export data_path="/home/ekoch/scratch/VLAXL_imaging/MeasurementSets/"

export casa_executable="/home/ekoch/casa-6.6.1-17-pipeline-2024.1.0.8/bin/casa"
export casa_script="/home/ekoch/lglbs_hi_scripts/fir_imaging/run_lglbs_HI_imaging.py"


export script_args="$this_galaxy $this_line_product $this_config $this_chunksize $this_idx"
echo "Args passed to script: $script_args"
xvfb-run -a $casa_executable --rcdir ~/.casa --nologger --nogui --log2term -c $casa_script $script_args
