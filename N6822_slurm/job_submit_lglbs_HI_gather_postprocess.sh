#!/bin/bash
#SBATCH --time=100:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=256G
#SBATCH --job-name=lglbs-hi-gather-postprocess-%J
#SBATCH --output=lglbs-hi-gather-postprocess-%J.out
#SBATCH --mail-user=ekoch@ualberta.ca
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# NGC6822 gather + postprocess job.
#
# Mirrors fir_imaging/job_submit_lglbs_HI_gather_postprocess.sh exactly,
# with N6822-specific defaults.  Arguments can be overridden at submission:
#
#   sbatch job_submit_lglbs_HI_gather_postprocess.sh [galaxy] [config] [line_product] [chunksize]
#
# Defaults:  ngc6822  A+B+C+D  hi21cm  20
#
# NOTE: argument order here is galaxy config line_product chunksize,
# matching run_lglbs_HI_gather_postprocess.py's sys.argv[-4:-1] parsing.

export this_galaxy=${1:-ngc6822}
export this_config=${2:-A+B+C+D}
export this_line_product=${3:-hi21cm}
export this_chunksize=${4:-20}

echo $SLURM_CPUS_PER_TASK

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load StdEnv
module load qt

source /home/ekoch/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/

export CASALD_LIBRARY_PATH=$LD_LIBRARY_PATH


# Ensure no time overlap in job start times
python3 -c "import time, random; time.sleep(random.randint(2, 120))"

export casa_executable="/home/ekoch/casa-6.6.1-17-pipeline-2024.1.0.8/bin/casa"
export casa_script="/home/ekoch/lglbs_hi_scripts/fir_imaging/run_lglbs_HI_gather_postprocess.py"


export script_args="$this_galaxy $this_config $this_line_product $this_chunksize"
echo "Args passed to script: $script_args"
xvfb-run -a $casa_executable --rcdir ~/.casa --nologger --nogui --log2term -c $casa_script $script_args
