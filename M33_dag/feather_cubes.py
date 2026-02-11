"""
08/22/2024
Use uvcombine to feather a low-resolution and high-resolution cube together.
The available scaling factors are taylored to LGLBS, but can use generic cubes
User Inputs:
-s --sdcube - <required> name of single dish cube
-i --interfcube - <required> name of interferometer cube
-o --outpath - <required> output folder name
-f --sdfactor - <optional> single dish flux scaling factor
-g --galaxy - <optional>  Galaxy name to identify correct single dish flux scaling factor
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
parser.add_argument('-i', '--interfcube',
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

args, unknown = parser.parse_known_args()
## parse measurement set list & output
sd_cubename = args.sdcube
interf_cubename = args.interfcube
output_path = args.outpath

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
def read_cubes(interf_name, sdname):
    ## read in cubes
    vla_cube = SpectralCube.read(interf_name, use_dask = True, save_to_tmp_dir=True)
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

## function to spectrally resample lowres cube
def spectral_resample(lowres, highres):
    fwhm_factor = np.sqrt(8*np.log(2))
    current_resolution = np.abs(np.diff(lowres.spectral_axis)[0]).to(u.km / u.s)
    target_resolution = np.abs(np.diff(highres.spectral_axis)[0]).to(u.km / u.s)
    if current_resolution < target_resolution:
        gaussian_width = ((target_resolution**2 - current_resolution**2)**0.5 /
                        current_resolution / fwhm_factor)
        kernel = Gaussian1DKernel(gaussian_width.value)
        lowres_specsmooth = lowres.spectral_smooth(kernel)
    else:
        lowres_specsmooth = lowres
    # Resample to the same spectral axis
    lowres_specinterp = lowres_specsmooth.spectral_interpolate(highres.spectral_axis)
    return lowres_specinterp    

## function to perform spatial reprojection
def reproject_single_dish(sdcube_name, lowres, highres):
    # Do a per-channel version to avoid the problem
    sd_filename = Path(sdcube_name).name
    reproj_filename = output_path + f"/{sd_filename[:-5]}_highresmatch.fits"
    print(f"Copying {interf_cubename} to {reproj_filename}")
    #os.system(f"cp {interf_cubename} {reproj_filename}")
    print("Per channel reprojection")
    #with warnings.catch_warnings():
    #   warnings.filterwarnings("ignore", message="WCS1 is missing card")
    #   for this_chan in tqdm(range(highres.shape[0])):
    #       reproj_chan = lowres[this_chan].reproject(highres[this_chan].header)
    #       with fits.open(reproj_filename, mode="update", memmap=True) as hdulist:
    #           hdulist[0].data[this_chan] = reproj_chan
    #           hdulist.flush()
    #           del hdulist[0].data
    # Allow reading in the whole cube.
    ## re-write beam info to header and explicitly attach
    with fits.open(reproj_filename, mode = 'update', memmap=True) as hdulist:
        hdulist[0].header['BMAJ'] = 0.151667 ## deg
        hdulist[0].header['BMIN'] = 0.151667 ## deg
        hdulist[0].header['BPA'] = 0.0 ## deg
        hdulist.flush()     

    specinterp_reproj = SpectralCube.read(reproj_filename, use_dask = True, save_to_tmp_dir=True)
    specinterp_reproj.allow_huge_operations = True
    ## attach beam
    gbt_beam = Beam(546*u.arcsec)
    specinterp_reproj = specinterp_reproj.with_beam(gbt_beam, raise_error_jybm=False)
    return specinterp_reproj

## function to feather on a per-channel basis
def feather_per_channel(highres_cube, lowres_cube):
    highres_filename = Path(interf_cubename).name
    this_feathered_filename = output_path + f"/{interf_cubename[:-5]}_feathered.fits"
    print(f"Copying {interf_cubename} to {this_feathered_filename}")
    os.system(f"cp {interf_cubename} {this_feathered_filename}")
    print("per channel combination")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="WCS1 is missing card")
        for this_chan in tqdm(range(highres_cube.shape[0])):
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
    lowres_cube, highres_cube = read_cubes(interf_cubename, sd_cubename)

    # If needed, spectrally smooth the GBT cube
    #lowres_cube = spectral_resample(lowres_cube, highres_cube)

    # Grid the single dish data to the interferometer spatial grid
    lowres_reproject = reproject_single_dish(sd_cubename, lowres_cube, highres_cube)

    # Feather with the SD scale factor applied (per channel)
    feather_per_channel(lowres_reproject, highres_cube)

if __name__=='__main__':
    main()
    exit()
