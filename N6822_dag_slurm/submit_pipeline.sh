#!/bin/bash
#
# submit_pipeline.sh
# Master submission script — direct SLURM replacement for N6822_emission_dag.dag.
#
# Chains split_channels → image_channel → combine_images → feather_cubes
# using sbatch --dependency=afterok, preserving the same linear dependency
# structure as the HTCondor DAG PARENT/CHILD declarations.
#
# The untar_images step from the HTCondor DAG is eliminated: images are
# written directly to the shared filesystem by image_channel.sh, so no
# tarball extraction or renaming is needed before combine_images.
#
# Usage:
#   bash submit_pipeline.sh [OPTIONS]
#
# Options:
#   --skip-split      Skip split_channels (per-channel MSes already exist)
#   --restart         Use restart_image_channel instead of image_channel
#   --skip-feather    Stop after combine_images
#   --dry-run         Print sbatch commands without submitting
#
# All parameters are defined in config.sh.

set -euo pipefail

## ---------------------------------------------------------------------------
## Parse options
## ---------------------------------------------------------------------------

SKIP_SPLIT=false
USE_RESTART=false
SKIP_FEATHER=false
DRY_RUN=false

for arg in "$@"; do
    case $arg in
        --skip-split)   SKIP_SPLIT=true ;;
        --restart)      USE_RESTART=true ;;
        --skip-feather) SKIP_FEATHER=true ;;
        --dry-run)      DRY_RUN=true ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--skip-split] [--restart] [--skip-feather] [--dry-run]"
            exit 1 ;;
    esac
done

source "$(dirname "$0")/config.sh"

## ---------------------------------------------------------------------------
## Helper: sbatch with --parsable; honours --dry-run
## ---------------------------------------------------------------------------

sbatch_run() {
    # Usage: sbatch_run [extra_flags...] -- script [script_flags...]
    local flags=()
    while [[ $1 != "--" ]]; do flags+=("$1"); shift; done
    shift
    if $DRY_RUN; then
        echo "[dry-run] sbatch --parsable ${flags[*]} $*" >&2
        echo "DRY_RUN_JID"; return
    fi
    sbatch --parsable "${flags[@]}" "$@"
}

## ---------------------------------------------------------------------------
## Pre-flight: ensure output directories exist
## ---------------------------------------------------------------------------

mkdir -p "${LOGS_DIR}" "${MS_DIR}" "${IMAGES_DIR}"

echo "=== N6822 DAG-style SLURM Imaging Pipeline ==="
echo "SRC_NAME      : ${SRC_NAME}"
echo "MS_NAME       : ${MS_NAME}"
echo "Channels      : ${CHAN_START}–${CHAN_END} (${N_IMAGING_CHANS} total)"
echo "SCRIPTS_DIR   : ${SCRIPTS_DIR}"
echo ""

## ---------------------------------------------------------------------------
## Step 1 (DAG node J): split_channels
##   HTCondor: split_channels.sub  queue 50
##   SLURM   : --array=0-49
## ---------------------------------------------------------------------------

SPLIT_MAX=$(( SPLIT_N_JOBS - 1 ))
DEP=""

if $SKIP_SPLIT; then
    echo "[J] split_channels     → SKIPPED"
else
    echo "[J] Submitting split_channels   (array 0-${SPLIT_MAX}) ..."
    SPLIT_JID=$(sbatch_run \
        --array=0-${SPLIT_MAX} \
        -- "${SCRIPTS_DIR}/split_channels.sh")
    DEP="--dependency=afterok:${SPLIT_JID}"
    echo "    job ID: ${SPLIT_JID}"
fi

## ---------------------------------------------------------------------------
## Step 2 (DAG node K): image_channel  (or restart_image_channel)
##   HTCondor: image_channel.sub  queue 424
##   SLURM   : --array=0-423
## ---------------------------------------------------------------------------

IMG_MAX=$(( N_IMAGING_CHANS - 1 ))

if $USE_RESTART; then
    IMG_SCRIPT="${SCRIPTS_DIR}/restart_image_channel.sh"
    IMG_LABEL="restart_image_channel"
else
    IMG_SCRIPT="${SCRIPTS_DIR}/image_channel.sh"
    IMG_LABEL="image_channel"
fi

echo "[K] Submitting ${IMG_LABEL}   (array 0-${IMG_MAX}) ..."
IMAGE_JID=$(sbatch_run \
    --array=0-${IMG_MAX} \
    ${DEP} \
    -- "${IMG_SCRIPT}")
echo "    job ID: ${IMAGE_JID}"

## ---------------------------------------------------------------------------
## Step 3 (DAG node M): combine_images
##   HTCondor: combine_images.sub  queue 1
##   SLURM   : single job, --dependency waits for all imaging tasks
##
## NOTE: untar_images (DAG node L) is not needed here because image_channel.sh
## writes tclean output directly to IMAGES_DIR on the shared filesystem.
## ---------------------------------------------------------------------------

echo "[M] Submitting combine_images   (single job) ..."
COMBINE_JID=$(sbatch_run \
    --dependency=afterok:${IMAGE_JID} \
    -- "${SCRIPTS_DIR}/combine_images.sh")
echo "    job ID: ${COMBINE_JID}"

## ---------------------------------------------------------------------------
## Step 4 (DAG node N): feather_cubes
##   HTCondor: feather_cubes.sub  queue 1
##   SLURM   : single job
## ---------------------------------------------------------------------------

if $SKIP_FEATHER; then
    echo "[N] feather_cubes      → SKIPPED"
else
    echo "[N] Submitting feather_cubes    (single job) ..."
    FEATHER_JID=$(sbatch_run \
        --dependency=afterok:${COMBINE_JID} \
        -- "${SCRIPTS_DIR}/feather_cubes.sh")
    echo "    job ID: ${FEATHER_JID}"
fi

echo ""
echo "Monitor with:"
echo "  squeue -u \$USER"
echo "  tail -f ${LOGS_DIR}/image_channel_${IMAGE_JID}_<TASK>.out"
