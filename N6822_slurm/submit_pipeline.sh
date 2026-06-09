#!/bin/bash
#
# submit_pipeline.sh
# Submit the two-step NGC6822 HI imaging pipeline with SLURM job dependencies.
#
# Replaces the HTCondor DAG (N6822_emission_dag.dag) with standard SLURM
# dependency chaining.  Both steps use the phangsPipeline ImagingChunkedHandler,
# mirroring the fir_imaging/ approach.
#
# Usage:
#   bash submit_pipeline.sh [OPTIONS]
#
# Options:
#   -g GALAXY        Galaxy key name            (default: ngc6822)
#   -l LINE          Line product name           (default: hi21cm)
#   -c CONFIG        Interferometer config        (default: A+B+C+D)
#   -n CHUNKSIZE     Channels per imaging chunk   (default: 20)
#   -N NCHUNKS       Number of imaging chunks     (default: 22)
#                    Sets --array=1-NCHUNKS on the imaging job.
#   --dry-run        Print sbatch commands without submitting

set -euo pipefail

## ---------------------------------------------------------------------------
## Defaults
## ---------------------------------------------------------------------------

GALAXY="ngc6822"
LINE="hi21cm"
CONFIG="A+B+C+D"
CHUNKSIZE=20
NCHUNKS=22
DRY_RUN=false

SCRIPTS_DIR="$(dirname "$(realpath "$0")")"

## ---------------------------------------------------------------------------
## Parse options
## ---------------------------------------------------------------------------

while [[ $# -gt 0 ]]; do
    case $1 in
        -g) GALAXY="$2";    shift 2 ;;
        -l) LINE="$2";      shift 2 ;;
        -c) CONFIG="$2";    shift 2 ;;
        -n) CHUNKSIZE="$2"; shift 2 ;;
        -N) NCHUNKS="$2";   shift 2 ;;
        --dry-run) DRY_RUN=true; shift ;;
        *)
            echo "Usage: $0 [-g galaxy] [-l line] [-c config] [-n chunksize] [-N nchunks] [--dry-run]"
            exit 1
            ;;
    esac
done

## ---------------------------------------------------------------------------
## Helper
## ---------------------------------------------------------------------------

sbatch_run() {
    # All extra sbatch flags are passed before "--", positional args after.
    local extra_args=()
    while [[ $1 != "--" ]]; do
        extra_args+=("$1")
        shift
    done
    shift

    if $DRY_RUN; then
        echo "[dry-run] sbatch --parsable ${extra_args[*]} $*"
        echo "DRY_RUN_JID"
        return
    fi
    sbatch --parsable "${extra_args[@]}" "$@"
}

## ---------------------------------------------------------------------------
## Summary
## ---------------------------------------------------------------------------

echo "=== NGC6822 SLURM Imaging Pipeline ==="
echo "  galaxy    : ${GALAXY}"
echo "  line      : ${LINE}"
echo "  config    : ${CONFIG}"
echo "  chunksize : ${CHUNKSIZE}  (nchunks: ${NCHUNKS}, array: 1-${NCHUNKS})"
echo ""

## ---------------------------------------------------------------------------
## Step 1: chunked imaging (array job, one task per chunk)
## ---------------------------------------------------------------------------

echo "[1/2] Submitting imaging array (1-${NCHUNKS}) ..."

IMAGING_JID=$(sbatch_run \
    --array=1-${NCHUNKS} \
    -- \
    "${SCRIPTS_DIR}/job_submit_lglbs_HI_imaging.sh" \
    "${GALAXY}" "${LINE}" "${CONFIG}" "${CHUNKSIZE}")

echo "      imaging job ID: ${IMAGING_JID}"

## ---------------------------------------------------------------------------
## Step 2: gather chunks into cube + postprocess
## Waits for ALL imaging array tasks to complete successfully.
## ---------------------------------------------------------------------------

echo "[2/2] Submitting gather + postprocess (dependency: afterok:${IMAGING_JID}) ..."

GATHER_JID=$(sbatch_run \
    --dependency=afterok:${IMAGING_JID} \
    -- \
    "${SCRIPTS_DIR}/job_submit_lglbs_HI_gather_postprocess.sh" \
    "${GALAXY}" "${CONFIG}" "${LINE}" "${CHUNKSIZE}")

echo "      gather job ID : ${GATHER_JID}"

echo ""
echo "Monitor with:"
echo "  squeue -u \$USER"
echo "  tail -f lglbs-hi-imaging-${IMAGING_JID}-<TASK>.out"
