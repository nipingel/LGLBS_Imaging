
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


def main():
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
    sys.path.append('uvcombine/uvcombine')
    from uvcombine import feather_simple_cube
    from pathlib import Path

    output_path = Path(output_path)

    vla_cube = SpectralCube.read(interf_cubename)
    vla_cube.allow_huge_operations = True

    gbt_cube = SpectralCube.read(sd_cubename)
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

    # VLA spatial mask. Account for coverage across all channels (in case some are empty)
    vla_spatial_mask = np.any(vla_cube.mask.include(), axis=0)

    # If needed, spectrally smooth the GBT cube
    fwhm_factor = np.sqrt(8*np.log(2))
    current_resolution = np.abs(np.diff(gbt_cube.spectral_axis)[0]).to(u.km / u.s)
    target_resolution = np.abs(np.diff(vla_cube.spectral_axis)[0]).to(u.km / u.s)

    if current_resolution < target_resolution:
        gaussian_width = ((target_resolution**2 - current_resolution**2)**0.5 /
                        current_resolution / fwhm_factor)
        # print(gaussian_width)
        kernel = Gaussian1DKernel(gaussian_width.value)
        gbt_cube_specsmooth = gbt_cube.spectral_smooth(kernel)
    else:
        gbt_cube_specsmooth = gbt_cube

    # Resample to the same spectral axis
    gbt_cube_specinterp = gbt_cube_specsmooth.spectral_interpolate(vla_cube.spectral_axis)

    # Grid the GBT data to the VLA grid
    ## The full cube reprojection is failing in some cases. I don't understand why.
    # target_hdr = vla_cube.header.copy()
    # target_hdr['TIMESYS'] = target_hdr['TIMESYS'].lower()
    # gbt_cube_specinterp_reproj = gbt_cube_specinterp.reproject(target_hdr)
    # gbt_cube_specinterp_reproj.to(u.K).write(sd_data_path / f"{this_gbt_filename[:-5]}_vlamatch_{this_key}_reproj.fits",
    #                                           overwrite=True)

    # Do a per-channel version to avoid the problem
    this_sd_filename = Path(sd_cubename).name
    gbt_reproj_filename = output_path / f"{this_sd_filename[:-5]}_vlamatch.fits"
    # Generate a copy of the VLA cube
    if gbt_reproj_filename.exists():
        gbt_reproj_filename.unlink()

    print(f"Copying {interf_cubename} to {gbt_reproj_filename}")
    os.system(f"cp {interf_cubename} {gbt_reproj_filename}")

    print("Per channel reprojection")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="WCS1 is missing card")
        for this_chan in tqdm(range(vla_cube.shape[0])):
            reproj_chan = gbt_cube_specinterp[this_chan].reproject(vla_cube[this_chan].header)

            # Apply the VLA spatial mask:
            reproj_chan[~vla_spatial_mask] = np.nan

            with fits.open(gbt_reproj_filename, mode="update") as hdulist:
                hdulist[0].data[this_chan] = reproj_chan

                hdulist.flush()

    # Allow reading in the whole cube.
    gbt_cube_specinterp_reproj = SpectralCube.read(gbt_reproj_filename)
    gbt_cube_specinterp_reproj.allow_huge_operations = True

    # Feather with the SD scale factor applied
    feathered_cube = feather_simple_cube(vla_cube.to(u.K),
                                    gbt_cube_specinterp_reproj.to(u.K),
                                    allow_lo_reproj=False,
                                    allow_spectral_resample=False,
                                    lowresscalefactor=sdfactor)

    # NaN out blank areas post-FFT.
    feathered_cube = feathered_cube.with_mask(vla_cube.mask)

    interf_cubename_only = Path(interf_cubename).name

    this_feathered_filename = output_path / f"{interf_cubename_only[:-5]}_feathered.fits"

    feathered_cube.write(this_feathered_filename, overwrite=True)

    # Append the scfactor used into the header.
    with fits.open(this_feathered_filename, mode="update") as hdulist:
        hdulist[0].header["COMMENT"] = f"Feathered with uvcombine using scfactor={scfactor}"
        hdulist.flush()

    # Clean up the intermediate files:
    if gbt_reproj_filename.exists():
        gbt_reproj_filename.unlink()

if __name__=='__main__':

	main()
	exit()
