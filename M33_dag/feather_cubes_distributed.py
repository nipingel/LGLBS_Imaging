"""
03/31/2025
Use uvcombine to feather a low-resolution and high-resolution cube together over
user-provided channel range. It assumes that disk space has been allocated and single
dish has been regridded
The available scaling factors are taylored to LGLBS, but can use generic cubes
User Inputs:
-s --sdcube - <required> name of single dish cube
-i --feathercube - <required> name of feather cube
-o --outpath - <required> output folder name
-f --sdfactor - <optional> single dish flux scaling factor
-g --galaxy - <optional>  Galaxy name to identify correct single dish flux scaling factor
-b --beginning_chan - <required> first channel in range to featehr
-l --last_chan - <required> last channel in range to feather
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
"""

## imports
import os
import warnings
from tqdm import tqdm
from astropy.io import fits
import numpy as np
import astropy.units as u
from astropy.convolution import Gaussian1DKernel
from spectral_cube import SpectralCube
from radio_beam import Beam
import sys
from pathlib import Path
import os
sys.path.append('uvcombine/uvcombine')
from uvcombine import feather_simple
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sdcube',
                    help='<required> name of single dish cube',
                    required = True,
                    type=str)
parser.add_argument('-i', '--feathercube',
                    help = '<required> name of interferometer cube',
                    required = True,
                    type=str)
parser.add_argument('-o', '--outpath',
                    help = '<required> output folder name',
                    required = True,
                    type=str)
parser.add_argument('-f', '--sdfactor',
                    help = '<optional> single dish flux scaling factor',
                    required=False,
                    type=float)
parser.add_argument('-g', '--galaxy',
                    help = '<optional> Galaxy name to identify correct single dish flux scaling factor',
                    required=False,
                    type=str)
parser.add_argument('-b', '--beginning_channel',
                    help = '<required> first channel in range to feather',
                    required=True,
                    type=int)
parser.add_argument('-l', '--last_channel',
                    help = '<required> last channel in range to feather',
                    required=True,
                    type=int)


args, unknown = parser.parse_known_args()
## parse measurement set list & output
sd_cubename = args.sdcube
feaher_cubename = args.feathercube
output_path = args.outpath
start_chan = args.beginning_channel
end_chan = args.last_channel

# We only have 6 targets so let's just hardcode the GBT-VLA flux scaling factors
scale_factors = {'wlm': 1.14,
                 'ic10': 0.96,
                 'ngc6822': 0.92,
                 'ic1613': None,
                 'm33': 1.0,  # Koch+18
                 'm31': None}
galaxy = args.galaxy
if galaxy is not None:
    if galaxy not in scale_factors:
         raise KeyError(f"{galaxy} not a valid galaxy name in the scale_factors dictionary.")
    sdfactor = scale_factors[galaxy]
else:
    sdfactor = args.sdfactor
if sdfactor is None:
     raise ValueError("sdfactor must be provided with -f or --sdfactor OR a valid galaxy "
                      "name must be provided with -g or --galaxy.")

## function to read/return cubes and beam parameters
def read_cubes(feather_name, sdname):
    ## read in cubes
    vla_cube = SpectralCube.read(feather_name, use_dask = True, save_to_tmp_dir=True)
    vla_cube.allow_huge_operations = True
    gbt_cube = SpectralCube.read(sdname, use_dask = True, save_to_tmp_dir=True)
    gbt_cube.allow_huge_operations = True

    # Use the proper beam model size, not the one in the header!
    gbt_beam_model = Beam(area=3.69e5 *u.arcsec**2)
    gbt_beam_model.major.to(u.arcmin)
    gbt_cube = gbt_cube.with_beam(gbt_beam_model, raise_error_jybm=False)
    gbt_cube = gbt_cube.with_spectral_unit(u.km / u.s, velocity_convention='radio')
    
    # There is an issue with the F2F optical to radio conversion that is not being
    # handled during reprojection. Just set to VRAD if that's the case.
    if "F2F" in gbt_cube.wcs.wcs.ctype[2]:
        gbt_cube.wcs.wcs.ctype[2] = "VRAD"
        gbt_cube.mask._wcs.wcs.ctype[2] = "VRAD"
    return gbt_cube, vla_cube

## function to feather on a per-channel basis
def feather_per_channel(highres_cube, lowres_cube, start_chan, end_chan):
    highres_filename = Path(highres_cuben).name
    this_feathered_filename = output_path + f"/{interf_cubename[:-5]}_feathered.fits"
    print("per channel combination")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="WCS1 is missing card")
        for this_chan in tqdm(range(start_chan, end_chan)):
            feathered_chan = feather_simple(highres_cube[this_chan].to(u.K),
                lowres_cube[this_chan].to(u.K),
                lowresscalefactor=sdfactor)
            with fits.open(this_feathered_filename, mode="update", memmap=True) as hdulist:
                hdulist[0].data[this_chan] = feathered_chan
                hdulist.flush()
                del hdulist[0].data
    return

def main():

    ## get cubes
    lowres_cube, highres_cube = read_cubes(feather_cubename, sd_cubename)

    # Feather with the SD scale factor applied (per channel)
    feather_per_channel(highres_cube, lowres_cube)

if __name__=='__main__':
    main()
    exit()
