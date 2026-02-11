"""
04/02/2025
Gaussian smooth cube to user-provided resolution and interpolate onto a coarser grid
Additionally, produce integrated and peak intensity moments (.smooth.fits, 
.peak.fits, and .integrated.fits) appended
User Inputs:
-c --cube - <required> name of input cube
-t --target_resolution - <required> target resolution in km/s
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
"""

## imports
import numpy as np
from astropy import units as u
from astropy.convolution import Gaussian1DKernel
from spectral_cube import SpectralCube
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cube',
                    help='<required> name of input cube',
                    required = True,
                    type=str)
parser.add_argument('-t', '--target_resolution',
                    help='<required> target resolution in km/s',
                    required = True,
                    type=float)
args, unknown = parser.parse_known_args()

## parse input cube
input_cubename = args.cube
target_resolution = args.target_resolution * u.km/u.s

## function to read cube
def read_cube(input_cubename):
    cube = SpectralCube.read(f"{input_cubename}", 
        use_dask = True, 
        memmap=True)
    return cube

## function to read/return cubes and beam parameters
def smooth_cube(cube, input_cubename, target_resolution):
    fwhm_factor = np.sqrt(8*np.log(2))
    current_resolution = np.abs(cube.header['CDELT3'])/1000.0 * u.km/u.s
    pixel_scale = np.abs(cube.header['CDELT3'])/1000.0 * u.km/u.s
    gaussian_width = ((target_resolution**2 - current_resolution**2)**0.5 / pixel_scale / fwhm_factor)
    kernel = Gaussian1DKernel(gaussian_width.value)
    smoothed_cube = cube.spectral_smooth(kernel)
    
    ## interpolate to new axis
    signed_current_resolution = cube.header['CDELT3']
    spec_axis = cube.spectral_axis.value
    if signed_current_resolution < 0:
        new_spec_axis = np.arange(spec_axis[0], spec_axis[-1], -1*target_resolution.value*1000.0) * u.m/u.s
    else:
        new_spec_axis = np.arange(spec_axis[0], spec_axis[-1], target_resolution.value*1000.0) * u.m/u.s
    interp_cube = smoothed_cube.spectral_interpolate(new_spec_axis, suppress_smooth_warning=True)
    ## write to disk
    interp_cube.write(f"{input_cubename[:-5]}.smoothed.fits", overwrite=True)
    return interp_cube

## function to feather on a per-channel basis
def compute_moments(smoothed_cube, input_cubename):
    moment_0 = smoothed_cube.moment(order=0) 
    peak_image = smoothed_cube.max(axis = 0)
    
    ## write to disk
    moment_0.write(f"{input_cubename[:-5]}.integrated.fits")
    peak_image.write(f"{input_cubename[:-5]}.peak.fits")
    return

def main():

    ## read in cube
    cube = read_cube(input_cubename)

    ## smooth cube
    smoothed_cube = smooth_cube(cube, input_cubename, target_resolution)

    ## compute moments
    compute_moments(smoothed_cube, input_cubename)

if __name__=='__main__':
    main()
    exit()
