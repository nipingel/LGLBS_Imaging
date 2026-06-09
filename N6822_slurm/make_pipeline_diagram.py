"""
make_pipeline_diagram.py

Generate a comparison diagram of the HTCondor DAG vs. SLURM imaging pipelines
for NGC6822 HI.  Saves pipeline_comparison.png and pipeline_comparison.pdf
in the same directory as this script.

Run with:  python make_pipeline_diagram.py
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
BG          = '#F5F6FA'
HTC_HDR     = '#2E5FA3'   # HTCondor column header
SLURM_HDR   = '#B5530A'   # SLURM column header
PARALLEL_FC = '#3A7D44'   # green fill  – parallel / array jobs
SINGLE_FC   = '#5B6C8A'   # slate fill  – single sequential job
TEXT_W      = 'white'
BADGE_TEXT  = '#1A1A1A'
ARROW_C     = '#555566'
BRACKET_C   = '#8888AA'
MAP_C       = '#9999BB'
SEP_C       = '#CCCCDD'
ANNOT_C     = '#444455'

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rbox(ax, cx, cy, w, h, fc, label, sublabel=None, ec='white', lw=2, alpha=1.0, zorder=3):
    """Draw a rounded rectangle centred at (cx, cy)."""
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.12',
        facecolor=fc, edgecolor=ec, linewidth=lw,
        alpha=alpha, zorder=zorder,
    )
    ax.add_patch(patch)
    label_y = cy + (0.17 if sublabel else 0)
    ax.text(cx, label_y, label,
            ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=TEXT_W, zorder=zorder + 1)
    if sublabel:
        ax.text(cx, cy - 0.22, sublabel,
                ha='center', va='center',
                fontsize=8.0, color='#DDDDEE', zorder=zorder + 1,
                linespacing=1.4)


def badge(ax, cx, cy, w, h, text, fc, zorder=6):
    """Small count badge in the top-right corner of a box."""
    bw, bh = 1.05, 0.36
    bx = cx + w / 2 - bw - 0.05
    by = cy + h / 2 - bh - 0.05
    b = FancyBboxPatch((bx, by), bw, bh,
                       boxstyle='round,pad=0.04',
                       facecolor='white', edgecolor=fc,
                       linewidth=1.5, zorder=zorder)
    ax.add_patch(b)
    ax.text(bx + bw / 2, by + bh / 2, text,
            ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=fc, zorder=zorder + 1)


def varrow(ax, x, y0, y1, color=ARROW_C, lw=2.0):
    """Vertical downward arrow from y0 to y1 at x."""
    ax.annotate('',
                xy=(x, y1 + 0.07), xytext=(x, y0 - 0.07),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, mutation_scale=18),
                zorder=4)


def dep_label(ax, x, y, text, color=ANNOT_C):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=7.5, color=color, style='italic',
            bbox=dict(boxstyle='round,pad=0.2', fc=BG, ec='none', alpha=0.8))


# ---------------------------------------------------------------------------
# Figure canvas
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(18, 12))
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.axis('off')

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
ax.text(9.0, 11.6,
        'NGC6822 HI Imaging Pipeline: HTCondor DAG vs. SLURM',
        ha='center', va='center',
        fontsize=15, fontweight='bold', color='#1A1A2E')

# ---------------------------------------------------------------------------
# Column divider & headers
# ---------------------------------------------------------------------------
ax.axvline(9.0, ymin=0.03, ymax=0.93, color=SEP_C, lw=1.8, ls='--', zorder=0)

for x, label, sub, col in [
    (4.5,  'HTCondor DAG', 'N6822_dag/', HTC_HDR),
    (13.5, 'SLURM',        'N6822_slurm/', SLURM_HDR),
]:
    ax.text(x, 11.1, label, ha='center', va='center',
            fontsize=13, fontweight='bold', color=col)
    ax.text(x, 10.75, sub, ha='center', va='center',
            fontsize=9, color='#666677', style='italic')

# ---------------------------------------------------------------------------
# HTCondor DAG  –  5 steps, equally spaced
# ---------------------------------------------------------------------------
HTC_X  = 4.5
BOX_W  = 7.2
BOX_H  = 1.05

# y centres top → bottom
htc_ys = [9.2, 7.7, 6.2, 4.7, 3.1]

htc_steps = [
    # (label, sublabel, fc, badge_text)
    ('Split Channels',
     'split_channels.sub  ·  split_channels.py\nCASA split()  ·  Docker nipingel/casa',
     PARALLEL_FC, '50 jobs'),
    ('Image Channel',
     'image_channel.sub  ·  image_channel.py\nCASA tclean()  ·  Docker nipingel/casa',
     PARALLEL_FC, '424 jobs'),
    ('Untar Images',
     'untar_images.sub  ·  untar_images.sh\nExtract .image files from tarballs',
     PARALLEL_FC, '131 jobs'),
    ('Combine Images',
     'combine_images.sub  ·  combine_images.py\nCASA ia.imageconcat  +  imsmooth  +  exportfits',
     SINGLE_FC, '1 job'),
    ('Feather Cubes',
     'feather_cubes.sub  ·  feather_cubes.py\nuvcombine.feather_simple_cube',
     SINGLE_FC, '1 job'),
]

for (label, sub, fc, bdg), y in zip(htc_steps, htc_ys):
    rbox(ax, HTC_X, y, BOX_W, BOX_H, fc, label, sub)
    badge(ax, HTC_X, y, BOX_W, BOX_H, bdg, fc)

# Arrows between HTCondor steps
for i in range(len(htc_ys) - 1):
    varrow(ax, HTC_X, htc_ys[i] - BOX_H / 2, htc_ys[i + 1] + BOX_H / 2)

# Dependency method label beside each arrow
dep_xs = [HTC_X + BOX_W / 2 + 0.65] * 4
dep_ys = [(htc_ys[i] + htc_ys[i + 1]) / 2 for i in range(4)]
dep_labels_htc = ['PARENT→CHILD', 'PARENT→CHILD', 'PARENT→CHILD', 'PARENT→CHILD']
for x, y, txt in zip(dep_xs, dep_ys, dep_labels_htc):
    dep_label(ax, x, y, txt)

# ---------------------------------------------------------------------------
# SLURM  –  2 steps
# ---------------------------------------------------------------------------
SLURM_X = 13.5

# Make imaging box taller; gather box taller to hold more text
IMG_H   = 2.05   # imaging chunk box
GTHR_H  = 2.8    # gather+postprocess box

slurm_img_y  = 8.2
slurm_gthr_y = 3.6

rbox(ax, SLURM_X, slurm_img_y,  BOX_W, IMG_H,  PARALLEL_FC,
     'Imaging Chunks',
     'job_submit_lglbs_HI_imaging.sh\nrun_lglbs_HI_imaging.py\nImagingChunkedHandler.run_imaging(chunk_num=i - 1)')
badge(ax, SLURM_X, slurm_img_y, BOX_W, IMG_H, '22 tasks', PARALLEL_FC)

rbox(ax, SLURM_X, slurm_gthr_y, BOX_W, GTHR_H, SINGLE_FC,
     'Gather + Postprocess',
     'job_submit_lglbs_HI_gather_postprocess.sh\nrun_lglbs_HI_gather_postprocess.py\n'
     'gather_into_cubes()  ·  loop_postprocess()\n'
     'pb-correction  ·  feathering  ·  mosaic')
badge(ax, SLURM_X, slurm_gthr_y, BOX_W, GTHR_H, '1 job', SINGLE_FC)

# Arrow between SLURM steps
slurm_arr_y0 = slurm_img_y  - IMG_H  / 2
slurm_arr_y1 = slurm_gthr_y + GTHR_H / 2
varrow(ax, SLURM_X, slurm_arr_y0, slurm_arr_y1, color=ARROW_C, lw=2.2)
dep_label(ax, SLURM_X + BOX_W / 2 + 0.95,
          (slurm_arr_y0 + slurm_arr_y1) / 2,
          '--dependency=\nafterok:$JID')

# ---------------------------------------------------------------------------
# Mapping brackets: HTCondor group → SLURM box
# ---------------------------------------------------------------------------

def mapping_bracket(ax, htc_top, htc_bot, slurm_mid,
                    color=BRACKET_C, lw=1.6, arrow_color=MAP_C):
    """
    Draw a right-facing brace on the HTCondor side spanning htc_top→htc_bot,
    then a dashed arrow across the separator to the SLURM box centre.
    """
    bx = HTC_X + BOX_W / 2 + 0.08  # right edge of HTCondor boxes
    mid = (htc_top + htc_bot) / 2

    # Bracket lines  (⌐ shape)
    ax.plot([bx, bx + 0.25, bx + 0.25, bx],
            [htc_top, htc_top, htc_bot, htc_bot],
            color=color, lw=lw, solid_capstyle='round', zorder=3)

    # Dashed arrow across to SLURM
    ax.annotate('',
                xy=(SLURM_X - BOX_W / 2 - 0.08, slurm_mid),
                xytext=(bx + 0.25, mid),
                arrowprops=dict(
                    arrowstyle='->', color=arrow_color,
                    lw=1.6, mutation_scale=14,
                    connectionstyle='arc3,rad=0.0',
                    linestyle='dashed'),
                zorder=3)


# Group 1: Split Channels + Image Channel + Untar Images  →  Imaging Chunks
g1_top = htc_ys[0] + BOX_H / 2
g1_bot = htc_ys[2] - BOX_H / 2
mapping_bracket(ax, g1_top, g1_bot, slurm_img_y)

# Group 2: Combine Images + Feather Cubes  →  Gather + Postprocess
g2_top = htc_ys[3] + BOX_H / 2
g2_bot = htc_ys[4] - BOX_H / 2
mapping_bracket(ax, g2_top, g2_bot, slurm_gthr_y)

# ---------------------------------------------------------------------------
# Key-differences footer
# ---------------------------------------------------------------------------
FOOT_Y = 1.55
ax.axhline(FOOT_Y - 0.35, color=SEP_C, lw=1.2, ls='-')

cols = {
    'Scheduler': (['condor_submit_dag', ''], ['sbatch --dependency', 'afterok:<jid>']),
    'Parallelism': (['queue N  per .sub', '(HTCondor job array)'], ['#SBATCH --array=1-N', '(SLURM array job)']),
    'Execution env': (['Docker container', 'nipingel/casa:latest'], ['module load StdEnv/qt', '+ local CASA binary']),
    'File I/O': (['Tarballs transferred', 'to execute node'], ['Shared scratch', 'filesystem (no tar)']),
    'Parallelism\ngranularity': (['1 chan / job', '(424 jobs total)'], ['~20 chans / task', '(22 tasks total)']),
}

ax.text(8.5, FOOT_Y + 0.65, 'Key Differences', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#333344')

col_xs = [1.6, 4.6, 7.7, 11.0, 14.5]
for (key, (htc_vals, slurm_vals)), cx in zip(cols.items(), col_xs):
    ax.text(cx, FOOT_Y + 0.3, key, ha='center', va='center',
            fontsize=8, fontweight='bold', color='#333344')
    ax.text(cx, FOOT_Y - 0.0, htc_vals[0], ha='center', va='center',
            fontsize=7.5, color=HTC_HDR)
    ax.text(cx, FOOT_Y - 0.28, htc_vals[1], ha='center', va='center',
            fontsize=7, color=HTC_HDR)
    ax.text(cx, FOOT_Y - 0.58, slurm_vals[0], ha='center', va='center',
            fontsize=7.5, color=SLURM_HDR)
    ax.text(cx, FOOT_Y - 0.86, slurm_vals[1], ha='center', va='center',
            fontsize=7, color=SLURM_HDR)

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
legend_handles = [
    mpatches.Patch(color=PARALLEL_FC, label='Parallel / array jobs'),
    mpatches.Patch(color=SINGLE_FC,   label='Single sequential job'),
    mpatches.Patch(color=MAP_C, alpha=0.7, label='Stage mapping (HTCondor → SLURM)'),
]
ax.legend(handles=legend_handles,
          loc='lower right', bbox_to_anchor=(0.99, 0.01),
          fontsize=8.5, framealpha=0.9, edgecolor=SEP_C)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.dirname(os.path.abspath(__file__))
for ext in ('png', 'pdf'):
    path = os.path.join(out_dir, f'pipeline_comparison.{ext}')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f'Saved: {path}')

plt.close(fig)
