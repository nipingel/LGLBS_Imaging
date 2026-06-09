"""
make_pipeline_diagram.py

Comparison diagram: HTCondor DAG vs DAG-style SLURM per-channel pipeline.
Both sides share the same Python scripts and per-channel step structure;
only the scheduler infrastructure changes.

Saves pipeline_comparison.png and pipeline_comparison.pdf in the same directory.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BG          = '#F5F6FA'
HTC_HDR     = '#2E5FA3'
SLURM_HDR   = '#B5530A'
PARALLEL_FC = '#3A7D44'   # green – parallel / array jobs
SINGLE_FC   = '#5B6C8A'   # slate – single sequential job
ELIM_FC     = '#8B2020'   # red   – eliminated step
ELIM_EDGE   = '#CC4444'
TEXT_W      = 'white'
ARROW_C     = '#555566'
EQUIV_C     = '#7799CC'   # blue dashes – 1-to-1 equivalent step
ELIM_C      = '#CC5555'   # red dashes  – eliminated step
SEP_C       = '#CCCCDD'
ANNOT_C     = '#444455'


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def rbox(ax, cx, cy, w, h, fc, label, sublabel=None,
         ec='white', lw=2, alpha=1.0, zorder=3, strikethrough=False):
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.12',
        facecolor=fc, edgecolor=ec, linewidth=lw,
        alpha=alpha, zorder=zorder,
    )
    ax.add_patch(patch)
    label_y = cy + (0.18 if sublabel else 0)
    ax.text(cx, label_y, label,
            ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=TEXT_W, zorder=zorder + 1)
    if sublabel:
        ax.text(cx, cy - 0.24, sublabel,
                ha='center', va='center',
                fontsize=7.8, color='#DDDDEE', zorder=zorder + 1,
                linespacing=1.35)
    if strikethrough:
        ax.plot([cx - w / 2 + 0.15, cx + w / 2 - 0.15], [cy, cy],
                color='#FF8888', lw=3, zorder=zorder + 2, solid_capstyle='round')


def badge(ax, cx, cy, w, h, text, fc, zorder=6):
    bw, bh = 1.1, 0.37
    bx = cx + w / 2 - bw - 0.06
    by = cy + h / 2 - bh - 0.06
    b = FancyBboxPatch((bx, by), bw, bh,
                       boxstyle='round,pad=0.04',
                       facecolor='white', edgecolor=fc,
                       linewidth=1.5, zorder=zorder)
    ax.add_patch(b)
    ax.text(bx + bw / 2, by + bh / 2, text,
            ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=fc, zorder=zorder + 1)


def varrow(ax, x, y0, y1, color=ARROW_C, lw=2.0, ls='-'):
    ax.annotate('',
                xy=(x, y1 + 0.07), xytext=(x, y0 - 0.07),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, mutation_scale=18,
                                linestyle=ls),
                zorder=4)


def dep_label(ax, x, y, text, color=ANNOT_C):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=7.2, color=color, style='italic',
            bbox=dict(boxstyle='round,pad=0.2', fc=BG, ec='none', alpha=0.85))


def mapping_arrow(ax, x0, y0, x1, y1, color=EQUIV_C, ls='dashed', label=None):
    """Horizontal dashed arrow between corresponding steps."""
    ax.annotate('',
                xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=1.7, mutation_scale=14,
                                connectionstyle='arc3,rad=0.0',
                                linestyle=ls),
                zorder=3)
    if label:
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ax.text(mx, my + 0.18, label, ha='center', va='bottom',
                fontsize=7, color=color, style='italic')


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(18, 13))
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
ax.set_xlim(0, 18)
ax.set_ylim(0, 13)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.axis('off')

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
ax.text(9.0, 12.6,
        'NGC6822 HI Imaging Pipeline: HTCondor DAG vs. DAG-style SLURM',
        ha='center', va='center',
        fontsize=14.5, fontweight='bold', color='#1A1A2E')
ax.text(9.0, 12.25,
        'Same per-channel Python scripts on both sides · scheduler infrastructure only changes',
        ha='center', va='center', fontsize=9.5, color='#555566', style='italic')

# ---------------------------------------------------------------------------
# Column separator & headers
# ---------------------------------------------------------------------------
ax.axvline(9.0, ymin=0.04, ymax=0.94, color=SEP_C, lw=1.8, ls='--', zorder=0)

for cx, label, sub, col in [
    (4.5,  'HTCondor DAG',        'N6822_dag/',       HTC_HDR),
    (13.5, 'DAG-style SLURM',     'N6822_dag_slurm/', SLURM_HDR),
]:
    ax.text(cx, 11.8, label, ha='center', va='center',
            fontsize=13, fontweight='bold', color=col)
    ax.text(cx, 11.45, sub, ha='center', va='center',
            fontsize=9, color='#666677', style='italic')

# ---------------------------------------------------------------------------
# Step definitions
# ---------------------------------------------------------------------------
BW    = 7.4    # box width
BH    = 1.05   # box height
HTC_X = 4.5
SLM_X = 13.5

# HTCondor y-centres, top → bottom
HY = [10.7, 9.25, 7.8, 6.35, 4.85]

htc_steps = [
    # (label, sublabel, fc, badge, dag_node)
    ('Split Channels',
     'split_channels.sub · split_channels.py\nCASA split() · Docker nipingel/casa · queue 50',
     PARALLEL_FC, '50 jobs', 'J'),
    ('Image Channel',
     'image_channel.sub · image_channel.py\nCASA tclean() · Docker nipingel/casa · queue 424',
     PARALLEL_FC, '424 jobs', 'K'),
    ('Untar Images',
     'untar_images.sub · untar_images.sh\nExtract & rename .image files from per-node tarballs · queue 131',
     PARALLEL_FC, '131 jobs', 'L'),
    ('Combine Images',
     'combine_images.sub · combine_images.py\nCASA ia.imageconcat + imsmooth + exportfits · queue 1',
     SINGLE_FC, '1 job', 'M'),
    ('Feather Cubes',
     'feather_cubes.sub · feather_cubes.py\nuvcombine.feather_simple_cube · queue 1',
     SINGLE_FC, '1 job', 'N'),
]

for (label, sub, fc, bdg, node), y in zip(htc_steps, HY):
    rbox(ax, HTC_X, y, BW, BH, fc, label, sub)
    badge(ax, HTC_X, y, BW, BH, bdg, fc)
    ax.text(HTC_X - BW / 2 - 0.22, y, node,
            ha='right', va='center', fontsize=9, fontweight='bold',
            color=HTC_HDR, alpha=0.7)

# Arrows between HTCondor steps
for i in range(len(HY) - 1):
    varrow(ax, HTC_X, HY[i] - BH / 2, HY[i + 1] + BH / 2)
    dep_label(ax, HTC_X + BW / 2 + 0.7,
              (HY[i] + HY[i + 1]) / 2, 'PARENT→CHILD')

# ---------------------------------------------------------------------------
# SLURM steps  (same y positions; untar is eliminated)
# ---------------------------------------------------------------------------
SY = HY   # keep vertical positions aligned for readability

slurm_steps = [
    # (label, sublabel, fc, badge, eliminated, dag_node)
    ('Split Channels',
     'split_channels.sh · split_channels.py  (unchanged)\nCASA split() · module load + xvfb-run · --array=0-49',
     PARALLEL_FC, '50 tasks', False, 'J'),
    ('Image Channel',
     'image_channel.sh · image_channel.py  (unchanged)\nCASA tclean() · module load + xvfb-run · --array=0-423',
     PARALLEL_FC, '424 tasks', False, 'K'),
    ('Untar Images',
     'NOT NEEDED on shared filesystem\nImages written directly to IMAGES_DIR; no tarballs produced',
     ELIM_FC, '—', True, '—'),
    ('Combine Images',
     'combine_images.sh · combine_images.py  (unchanged)\nCASA ia.imageconcat + imsmooth + exportfits · 1 job',
     SINGLE_FC, '1 job', False, 'M'),
    ('Feather Cubes',
     'feather_cubes.sh · feather_cubes.py  (bugs fixed)\nuvcombine.feather_simple_cube · conda env · 1 job',
     SINGLE_FC, '1 job', False, 'N'),
]

for (label, sub, fc, bdg, elim, node), y in zip(slurm_steps, SY):
    ec = ELIM_EDGE if elim else 'white'
    lw = 2.5 if elim else 2.0
    al = 0.55 if elim else 1.0
    rbox(ax, SLM_X, y, BW, BH, fc, label, sub,
         ec=ec, lw=lw, alpha=al, strikethrough=elim)
    if elim:
        badge(ax, SLM_X, y, BW, BH, bdg, ELIM_EDGE)
        ax.text(SLM_X, y + BH / 2 + 0.18, '✕  eliminated',
                ha='center', va='bottom', fontsize=8,
                color=ELIM_EDGE, fontweight='bold')
    else:
        badge(ax, SLM_X, y, BW, BH, bdg, fc)
        ax.text(SLM_X - BW / 2 - 0.22, y, node,
                ha='right', va='center', fontsize=9, fontweight='bold',
                color=SLURM_HDR, alpha=0.7)

# Arrows between SLURM steps (skip the eliminated untar)
SLURM_FLOW = [(0, 1), (1, 3), (3, 4)]   # indices in SY that are connected
slurm_dep_labels = ['--dependency=\nafterok', '--dependency=\nafterok', '--dependency=\nafterok']
for (i, j), dlabel in zip(SLURM_FLOW, slurm_dep_labels):
    varrow(ax, SLM_X, SY[i] - BH / 2, SY[j] + BH / 2)
    dep_label(ax, SLM_X + BW / 2 + 0.75,
              (SY[i] + SY[j]) / 2, dlabel)

# Dotted bypass arrow from image_channel to combine_images (skipping untar)
bypass_x = SLM_X - BW / 2 - 0.45
ax.annotate('',
            xy=(bypass_x, SY[3] + BH / 2),
            xytext=(bypass_x, SY[1] - BH / 2),
            arrowprops=dict(arrowstyle='->', color=EQUIV_C,
                            lw=1.6, mutation_scale=14,
                            connectionstyle='arc3,rad=0.0',
                            linestyle='dotted'),
            zorder=3)
ax.text(bypass_x - 0.12, (SY[1] + SY[3]) / 2, 'bypass\n(no untar)',
        ha='right', va='center', fontsize=7.2,
        color=EQUIV_C, style='italic')

# ---------------------------------------------------------------------------
# Cross-column mapping arrows  (HTCondor right edge → SLURM left edge)
# ---------------------------------------------------------------------------
RX = HTC_X + BW / 2 + 0.08   # right edge HTCondor
LX = SLM_X - BW / 2 - 0.08   # left  edge SLURM

for idx, (color, ls, tip) in enumerate([
    (EQUIV_C, 'dashed',  '= same Python script'),   # split
    (EQUIV_C, 'dashed',  '= same Python script'),   # image
    (ELIM_C,  'dotted',  '✕ eliminated'),            # untar
    (EQUIV_C, 'dashed',  '= same Python script'),   # combine
    (EQUIV_C, 'dashed',  '≈ bugs fixed'),            # feather
]):
    y = HY[idx]
    ax.annotate('',
                xy=(LX, y), xytext=(RX, y),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=1.5, mutation_scale=13,
                                connectionstyle='arc3,rad=0.0',
                                linestyle=ls),
                zorder=3)
    ax.text((RX + LX) / 2, y + 0.32, tip,
            ha='center', va='bottom', fontsize=7,
            color=color, style='italic')

# ---------------------------------------------------------------------------
# Key differences footer
# ---------------------------------------------------------------------------
FOOT_Y = 3.55
ax.axhline(FOOT_Y - 0.35, color=SEP_C, lw=1.2)

ax.text(9.0, FOOT_Y + 0.72, 'Key Infrastructure Changes (Python scripts are identical)',
        ha='center', va='center', fontsize=10, fontweight='bold', color='#333344')

cols = {
    'Scheduler': (
        ['condor_submit_dag', 'PARENT/CHILD deps'],
        ['bash submit_pipeline.sh', '--dependency=afterok']),
    'Parallelism': (
        ['queue N  in .sub file', '(HTCondor array)'],
        ['#SBATCH --array=0-N-1', '(SLURM array)']),
    'Execution env': (
        ['Docker container', 'nipingel/casa:latest'],
        ['module load StdEnv/qt', 'xvfb-run + local CASA']),
    'File I/O': (
        ['Tarballs staged to', 'execute node + back'],
        ['Shared scratch', 'no transfer, no tar']),
    'Untar step': (
        ['Required (131 jobs)', 'rename + extract'],
        ['Eliminated', 'images written directly']),
}

col_xs = [1.7, 4.8, 8.1, 11.4, 14.9]
for (key, (htc_vals, slm_vals)), cx in zip(cols.items(), col_xs):
    ax.text(cx, FOOT_Y + 0.35, key, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#333344')
    ax.text(cx, FOOT_Y + 0.02,  htc_vals[0], ha='center', va='center',
            fontsize=7.5, color=HTC_HDR)
    ax.text(cx, FOOT_Y - 0.28, htc_vals[1], ha='center', va='center',
            fontsize=7,   color=HTC_HDR)
    ax.text(cx, FOOT_Y - 0.58, slm_vals[0], ha='center', va='center',
            fontsize=7.5, color=SLURM_HDR)
    ax.text(cx, FOOT_Y - 0.88, slm_vals[1], ha='center', va='center',
            fontsize=7,   color=SLURM_HDR)

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
legend_handles = [
    mpatches.Patch(color=PARALLEL_FC, label='Parallel / array jobs (same granularity)'),
    mpatches.Patch(color=SINGLE_FC,   label='Single sequential job'),
    mpatches.Patch(color=ELIM_FC,     label='Step eliminated in SLURM version'),
    mpatches.Patch(color=EQUIV_C,     label='Same Python script both sides'),
    mpatches.Patch(color=ELIM_C,      label='Step removed (no tarballs on shared filesystem)'),
]
ax.legend(handles=legend_handles,
          loc='lower right', bbox_to_anchor=(0.99, 0.01),
          fontsize=8, framealpha=0.9, edgecolor=SEP_C)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.dirname(os.path.abspath(__file__))
for ext in ('png', 'pdf'):
    path = os.path.join(out_dir, f'pipeline_comparison.{ext}')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f'Saved: {path}')

plt.close(fig)
