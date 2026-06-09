"""
Feather a VLA interferometer cube with a GBT single-dish cube using uvcombine.

User inputs:
-s --sdcube     <required>  path to single-dish (GBT) FITS cube
-i --interfcube <required>  path to interferometer (VLA) FITS cube
-o --outpath    <required>  output file path (FITS)
-f --sdfactor   <optional>  single-dish flux scaling factor (overridden by -g)
-g --galaxy     <optional>  galaxy name used to look up the known GBT-VLA scale factor

Source: based on N6822_dag/feather_cubes.py
Changes vs original:
  - Removed duplicate '-f/--sdfactor' argparse argument (caused runtime crash).
  - Fixed variable name 'scfactor' -> 'sdfactor' in FITS header COMMENT.
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sdcube',
                    help='<required> path to single-dish cube',
                    required=True, type=str)
parser.add_argument('-i', '--interfcube',
                    help='<required> path to interferometer cube',
                    required=True, type=str)
parser.add_argument('-o', '--outpath',
                    help='<required> output file path',
                    required=True, type=str)
parser.add_argument('-f', '--sdfactor',
                    help='<optional> single-dish flux scaling factor',
                    required=False, type=float)
parser.add_argument('-g', '--galaxy',
                    help='<optional> galaxy name to look up GBT-VLA scale factor',
                    required=False, type=str)
args, unknown = parser.parse_known_args()

sd_cubename     = args.sdcube
interf_cubename = args.interfcube
output_path     = args.outpath

# Known GBT-VLA flux scaling factors per galaxy
scale_factors = {
    'wlm':     1.14,
    'ic10':    0.96,
    'ngc6822': 0.92,
    'ic1613':  None,
    'm33':     1.0,
    'm31':     None,
}

galaxy = args.galaxy
if galaxy is not None:
    if galaxy not in scale_factors:
        raise KeyError(f"{galaxy} not a valid galaxy name in the scale_factors dictionary.")
    sdfactor = scale_factors[galaxy]
else:
    sdfactor = args.sdfactor

if sdfactor is None:
    raise ValueError(
        "sdfactor must be provided with -f/--sdfactor OR a valid galaxy name "
        "with -g/--galaxy."
    )


def main():
    from astropy.io import fits
    import numpy as np
    import astropy.units as u
    from astropy.convolution import Gaussian1DKernel
    from spectral_cube import SpectralCube
    from radio_beam import Beam
    from pathlib import Path
    from uvcombine import feather_simple_cube

    output_path_obj = Path(output_path)

    vla_cube = SpectralCube.read(interf_cubename)
    vla_cube.allow_huge_operations = True

    gbt_cube = SpectralCube.read(sd_cubename)
    gbt_cube.allow_huge_operations = True

    # Use the proper GBT beam model size (not the one in the header)
    gbt_beam_model = Beam(area=3.69e5 * u.arcsec**2)
    gbt_beam_model.major.to(u.arcmin)

    gbt_cube = gbt_cube.with_beam(gbt_beam_model, raise_error_jybm=False)
    gbt_cube = gbt_cube.with_spectral_unit(u.km / u.s, velocity_convention='radio')

    # Fix F2F optical-to-radio conversion not handled during reprojection
    if "F2F" in gbt_cube.wcs.wcs.ctype[2]:
        gbt_cube.wcs.wcs.ctype[2] = "VRAD"
        gbt_cube.mask._wcs.wcs.ctype[2] = "VRAD"

    # Spectrally smooth the GBT cube if its resolution is finer than the VLA cube
    fwhm_factor = np.sqrt(8 * np.log(2))
    current_resolution = np.abs(np.diff(gbt_cube.spectral_axis)[0]).to(u.km / u.s)
    target_resolution  = np.abs(np.diff(vla_cube.spectral_axis)[0]).to(u.km / u.s)

    if current_resolution < target_resolution:
        gaussian_width = ((target_resolution**2 - current_resolution**2)**0.5 /
                          current_resolution / fwhm_factor)
        kernel = Gaussian1DKernel(gaussian_width.value)
        gbt_cube_specsmooth = gbt_cube.spectral_smooth(kernel)
    else:
        gbt_cube_specsmooth = gbt_cube

    # CASA writes TIMESYS in caps; wcslib does not like that
    target_hdr = vla_cube.header.copy()
    target_hdr['TIMESYS'] = target_hdr['TIMESYS'].lower()

    # Interpolate GBT data onto the VLA spectral grid
    gbt_cube_specinterp = gbt_cube_specsmooth.spectral_interpolate(vla_cube.spectral_axis)

    # Reproject GBT data onto the VLA spatial grid
    gbt_cube_specinterp_reproj = gbt_cube_specinterp.reproject(target_hdr)
    gbt_cube_specinterp_reproj.allow_huge_operations = True

    # Apply the same primary-beam coverage mask as the VLA cube
    gbt_cube_specinterp_reproj = gbt_cube_specinterp_reproj.with_mask(
        np.isfinite(vla_cube[0])
    )

    # Feather with the SD scale factor applied
    feathered_cube = feather_simple_cube(
        vla_cube.to(u.K),
        gbt_cube_specinterp_reproj.to(u.K),
        allow_lo_reproj=False,
        allow_spectral_resample=False,
        lowresscalefactor=sdfactor,
    )

    # NaN out blank areas post-FFT
    feathered_cube = feathered_cube.with_mask(vla_cube.mask)

    interf_cubename_only = Path(interf_cubename).name
    this_feathered_filename = output_path_obj / f"{interf_cubename_only[:-5]}_feathered.fits"

    feathered_cube.write(this_feathered_filename, overwrite=True)

    # Record the scale factor used in the FITS header
    with fits.open(this_feathered_filename, mode="update") as hdulist:
        hdulist[0].header["COMMENT"] = (
            f"Feathered with uvcombine using sdfactor={sdfactor}"
        )
        hdulist.flush()


if __name__ == '__main__':
    main()
    exit()
