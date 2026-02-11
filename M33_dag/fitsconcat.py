"""
17/6/24
script based on Krishna Sekhar's script to concat individual spectral planes into PPV cube
see: https://github.com/Kitchi/fitsconcat/tree/main
User inputs:

Usage: 
python fitsconcat.py 
__author__ = "Nick Pingel"
__version__ = "1.0"
__email__ = "nmpingel@wisc.edu"
"""

##imports
import os
import glob
import argparse
import numpy as np
from spectral_cube import SpectralCube
from astropy.wcs import WCS
from astropy.io import fits
from astropy.convolution import convolve_fft
from astropy.wcs.utils import proj_plane_pixel_scales
import astropy.units as u
from radio_beam import Beam
from radio_beam.utils import deconvolve


## parse user arguments
def parse_user_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help = '<required> path to input FITS files', required = True)
    parser.add_argument('-e', '--extension', help = '<required> is the suffix *-beam.fits or *-image-pb.fits; valid input is beam or image-pb', required = True)
    parser.add_argument('-o', '--outname', help ='<required> output name of file (.fits automatically appended)', required = True)
    args, unknown = parser.parse_known_args()
    return args.path, args.outname, args.extension

## make empty FITS cube
## see https://docs.astropy.org/en/stable/io/fits/appendix/faq.html#how-can-i-create-a-very-large-fits-file-from-scratch
def make_empty_image(imlist, path, outname):
    """
    Generate an empty dummy FITS data cube. The FITS cube can exceed available
    RAM.

    The 2D image dimensions are derived from the first image in the list.
    The number of channels in the output cube is assumed to be the length
    of the input list of images.
    """

    with fits.open(imlist[0], memmap=True) as hud:
        xdim, ydim = np.squeeze(hud[0].data).shape[-2:]

    zdim = int(len(imlist))
    dims = tuple([zdim, ydim, xdim])
    print("X-dimension: ", xdim)
    print("Y-dimension: ", ydim)
    print("Z-dimension: ", zdim)
    print('\n')
    
    ## create dummy data - size is irrelevant, just number of dims
    data = np.zeros((0, 0, 0), dtype=np.float32)
    hdu = fits.PrimaryHDU(data=data)
    header = hdu.header
    ## make minimal header
    while len(header) < (36 * 1 - 1):
        header.append()  # Adds a blank card to the end

    ## update header with correct size
    header["NAXIS1"] = dims[1]
    header["NAXIS2"] = dims[2]
    header["NAXIS3"] = dims[0]
    header.tofile('%s/%s' % (path, outname))

    with open('%s/%s' % (path, outname), "rb+") as fobj:
        # Seek past the length of the header, plus the length of the
        # Data we want to write.
        # 4 is the number of bytes per value, i.e. abs(header['BITPIX'])/8
        # (this example is assuming a 32-bit float)
        file_length = len(header.tostring()) + (dims[0] * dims[1] * dims[2] * 4)
        # FITS files must be a multiple of 2880 bytes long; the final -1
        # is to account for the final byte that we are about to write.
        file_length = ((file_length + 2880 - 1) // 2880) * 2880 - 1
        fobj.seek(file_length)
        fobj.write(b"\0") ## writes zeros
    return

## add spectral axis to header of dummy cube
def get_target_bmaj(imlist):
    bmaj_list = []
    for l in imlist:
        hdu = fits.open(l)
        bmaj_list.append(hdu[0].header['BMAJ']*3600)
    target_bmaj = round(np.max(bmaj_list)*(1+0.05), 1) * u.arcsec ## make final beam 5% larger than largest beam size across images
    target_beam = Beam(major = target_bmaj, minor = target_bmaj, pa = 0 * u.deg)
    return target_beam

## smooth image to desired final common resolution
def smooth_image(hdu, target_beam):
    ## compute kernel beam
    orig_beam = Beam.from_fits_header(hdu[0].header)
    kernel_beam = target_beam.deconvolve(orig_beam)
    
    ## get pix scales for convolution
    wcs = WCS(hdu[0].header)
    pixscale_deg = proj_plane_pixel_scales(wcs)[0]
    pixscale = (pixscale_deg * u.deg).to(u.arcsec)
    kernel = kernel_beam.as_kernel(pixscale)
    smoothed_image = convolve_fft(hdu[0].data[0, :, :], kernel, 
        normalize_kernel=True, allow_huge=True, nan_treatment='interpolate')
    return smoothed_image

## fill cube with FITS images
def fill_cube_with_images(imlist, target_beam, path, outname):
    """
    Fills the empty data cube with fits data.

    The number of channels in the output cube is assumed to be the length
    of the input list of images.
    """
    ## open first image FITS to get header
    first_im_hdu = fits.open(imlist[0])

    ## open cube FITS
    outhdu = fits.open('%s/%s' % (path, outname), memmap=True, mode="update")
    outdata = outhdu[0].data

    max_chan =  int(len(imlist))
    for ii in range(0, max_chan):
        print(f"Processing channel {ii}/{max_chan}", end='\r')
        with fits.open(imlist[ii], memmap=True) as hdu:
            sm_image = smooth_image(hdu, target_beam)
            outdata[ii, :, :] = sm_image
    ## update fits file
    new_header = target_beam.attach_to_header(first_im_hdu[0].header, copy = True)
    fits.writeto('%s/%s' % (path, outname), outdata, header = new_header, overwrite = True)
    outhdu.close()

def main():
    ## parse user arguments (path to FITS files)
    fits_file_path, f_outname, f_ext = parse_user_arguments()
    cube_outname = '%s.fits' % (f_outname)
    print('%s/*.%s' % (fits_file_path, f_ext))
    image_list = sorted(glob.glob('%s/*.%s' % (fits_file_path, f_ext)))

    ## get target beam object for smoothing
    target_beam = get_target_bmaj(image_list)

    ## make empty FITS cube
    #make_empty_image(image_list, fits_file_path, cube_outname)

    ## fill FITS cube
    fill_cube_with_images(image_list, target_beam, fits_file_path, cube_outname)
if __name__ == '__main__':
    main()
