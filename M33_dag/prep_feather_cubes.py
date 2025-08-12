"""
08/07/2025
Prepare to perform distributed feather by creating a copy of the
VLA-only cube and reproject single dish cube
User Inputs:
-s --sdcube - <required> name of single dish cube
-i --interfcube - <required> name of interferometer cube
-f --feathercube - <required> name of cube to be feathered
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@iu.edu"
"""

## imports
import warnings
from tqdm import tqdm
from astropy.io import fits
import numpy as np
import astropy.units as u
from astropy.convolution import Gaussian1DKernel
from spectral_cube import SpectralCube
from radio_beam import Beam
from pathlib import Path
import sys
import os
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
parser.add_argument('-f', '--feathercube',
                    help = '<required> name of cube to be feathered',
                    required = True,
                    type=str)

## function to parse user arguments
def parse_inputs():
    args, unknown = parser.parse_known_args()
    sd_cubename = args.sdcube
    interf_cubename = args.interfcube
    feather_cubename = args.feathercube
    return sd_cubename, interf_cubename, feather_cubename

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
def reproject_single_dish(sdcube_name, interf_cubename, lowres, highres):
    # Do a per-channel version to avoid the problem
    sd_filename = Path(sdcube_name).name
    reproj_filename = f"{sd_filename[:-5]}_highresmatch.fits"
    print(f"Copying {interf_cubename} to {reproj_filename}")
    ## os.system(f"cp {interf_cubename} {reproj_filename}")
    print("Per channel reprojection")
    with warnings.catch_warnings():
       warnings.filterwarnings("ignore", message="WCS1 is missing card")
       for this_chan in tqdm(range(highres.shape[0])):
           reproj_chan = lowres[this_chan].reproject(highres[this_chan].header)
           with fits.open(reproj_filename, mode="update", memmap=True) as hdulist:
               hdulist[0].data[this_chan] = reproj_chan
               hdulist.flush()
               del hdulist[0].data
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
    return

## function to copy VLA-only cube
def copy_vla_only(interf_cubename, feather_cubename):
    print(f"Copying {interf_cubename} to {feather_cubename}")
    os.system(f"cp {interf_cubename} {feather_cubename}")
    return

def main():
    ## get user arguments
    sd_cubename, interf_cubename, feather_cubename = parse_inputs()

    ## get cubes
    lowres_cube, highres_cube = read_cubes(interf_cubename, sd_cubename)

    # If needed, spectrally smooth the GBT cube
    lowres_cube = spectral_resample(lowres_cube, highres_cube)

    # Grid the single dish data to the interferometer spatial grid
    reproject_single_dish(sd_cubename, interf_cubename, lowres_cube, highres_cube)

    # make copy of vla-only cube to place feathered channels on disk in next node
    copy_vla_only(interf_cubename, feather_cubename)

if __name__=='__main__':
    main()
    exit()
