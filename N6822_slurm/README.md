# N6822 SLURM Imaging Pipeline

SLURM replacement for the HTCondor DAG imaging pipeline in `../N6822_dag/`.

This pipeline uses the **phangsPipeline `ImagingChunkedHandler`**, mirroring
`lglbs_hi_scripts/fir_imaging/` exactly.  The per-channel CASA scripts from
`N6822_dag/` are not used here; the pipeline handler manages channel splitting,
imaging, and cube assembly internally.

---

## Files

| File | HTCondor DAG equivalent | Description |
|---|---|---|
| `job_submit_lglbs_HI_imaging.sh` | `image_channel.sub` + `split_channels.sub` | SBATCH array job: chunked HI imaging via `ImagingChunkedHandler` |
| `job_submit_lglbs_HI_gather_postprocess.sh` | `combine_images.sub` + `feather_cubes.sub` | SBATCH job: gather chunks into cube + primary beam correction + feathering |
| `submit_pipeline.sh` | `N6822_emission_dag.dag` | Chains the two steps with `--dependency=afterok` |

The Python scripts called by these jobs are the shared fir_imaging scripts:
- `run_lglbs_HI_imaging.py` (in `lglbs_hi_scripts/fir_imaging/`)
- `run_lglbs_HI_gather_postprocess.py` (in `lglbs_hi_scripts/fir_imaging/`)

No copies are kept here; the SBATCH scripts reference them by absolute path.

---

## How it differs from the HTCondor DAG

| HTCondor DAG | This SLURM pipeline |
|---|---|
| `condor_submit_dag N6822_emission_dag.dag` | `bash submit_pipeline.sh` |
| Per-channel `.sub` jobs for split, image, untar, combine, feather | Two SBATCH jobs: chunked imaging array + gather/postprocess |
| Docker container with CASA | Module-loaded env + local CASA binary |
| File staging via tarballs between nodes | Shared scratch filesystem (no tar/untar) |
| 424 individual HTCondor array tasks (one per channel) | ~22 SLURM array tasks (one per chunk of 20 channels) |
| Separate untar step to reassemble images | Not needed; `task_complete_gather_into_cubes()` handles it |
| Separate feather step | Handled by `PostProcessHandler.loop_postprocess()` |

---

## Prerequisites

1. **Staged measurement set** — the combined, statwt'd MS must be present.
   Run `fir_imaging/job_submit_lglbs_staging.sh ngc6822 A+B+C+D` first if not
   already done.

2. **Master key** — `ngc6822` must be listed in
   `/home/ekoch/lglbs_hi_scripts/lglbs_keys/master_key_fir.txt` (it is).

3. **CASA** — available at the path in the SBATCH scripts.

---

## Usage

### Full pipeline (submit both steps at once)

```bash
bash submit_pipeline.sh
```

This submits:
1. An imaging array job (`--array=1-22`) for ngc6822 hi21cm A+B+C+D
2. A gather+postprocess job that starts only when all 22 imaging tasks succeed

### Override defaults

```bash
# Different line product
bash submit_pipeline.sh -l himidres

# Different chunksize (fewer, larger chunks)
bash submit_pipeline.sh -n 40 -N 11

# Dry run to preview sbatch commands
bash submit_pipeline.sh --dry-run
```

### Submit steps individually

```bash
# Step 1: imaging chunks
sbatch --array=1-22 job_submit_lglbs_HI_imaging.sh ngc6822 hi21cm A+B+C+D 20

# Step 2: gather + postprocess (after imaging job 12345 completes)
sbatch --dependency=afterok:12345 \
    job_submit_lglbs_HI_gather_postprocess.sh ngc6822 A+B+C+D hi21cm 20
```

### Multiple line products

Submit one pipeline per line product.  Steps for different products are
independent and can run simultaneously:

```bash
for line in hi21cm himidres hilores; do
    bash submit_pipeline.sh -l ${line}
done
```

---

## Choosing NCHUNKS

The number of imaging chunks depends on the number of spectral channels in
the staged MS and the chunksize.  `ImagingChunkedHandler` computes `nchunks`
automatically; if `SLURM_ARRAY_TASK_ID > nchunks` the task exits gracefully.

| Line product | Approx. channels | chunksize=20 → nchunks |
|---|---|---|
| hi21cm (0.4 km/s) | ~525 | ~27 |
| hi21cm_0p8kms | ~265 | ~14 |
| himidres (2.1 km/s) | ~100 | ~5 |
| hilores (4.2 km/s) | ~50 | ~3 |

It is safe to set `-N` slightly larger than the actual nchunks.

---

## Monitoring

```bash
squeue -u $USER                              # all your jobs
squeue -u $USER -j <IMAGING_JID>            # imaging array progress
tail -f lglbs-hi-imaging-<JID>-<TASK>.out   # single task log
```
