"""
11/14/2i022
reweight measurement sets based on rms of emission-free channels
User inputs:
-v --vsys - systemic velocity of source (assumed LSRK)
-w --vwidth - velocity width of source
-n --msPath - path of measurement set
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse
import sys
sys.path.append('./analysis_scripts')
import numpy as np 
from scipy.ndimage import label
import analysisUtils as au
from astropy import units as u

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vsys', help='<required> systematic velocity (assumed LSRK)', type = int, required = True)
parser.add_argument('-w', '--vwidth', help='<required> velocity width', type = int, required = True)
parser.add_argument('-n', '--msPath', help = '<required> FULL path of ms file', required = True)
args, unknown = parser.parse_known_args()

## function to construct MW mask
def MW_indices(freq_arr):
	nu_0 = 1.42040575e9
	vel_axis= u.c.value*(1-freq_arr/nu_0)
	inds = ((vel_axis >= -200.0*1e3) * (vel_axis <= 200*1e3))
	return inds


## function to convert provided vsys and vwidth to high and low frequency ranges
def compute_freq_range_hz(vsys, vwidth):
	nu_0 = 1.42040575e9
	v_low = vsys - vwidth/2
	v_high = vsys + vwidth/2
	freq_low = nu_0*(1-v_low/u.c.value)
	freq_high = nu_0*(1-v_high/u.c.value)
	return freq_low, freq_high

## function to determine which relevant channel range to exclude (based on systematic velocity and expected velocity width)
def construct_spw_str(vsys, vwidth):
	vm = au.ValueMapping(msPath)
	freq_axis = vm.spwInfo[0]['chanFreqs']
	half_chan = abs(freq_axis[1]-freq_axis[0])*0.5
	chan_axis = np.arange(len(freq_axis))
	mask_axis = np.zeros_like(chan_axis, dtype='bool')
	first_string = True
	spw_flagging_string = ''

	low_freq_hz, high_freq_hz = compute_freq_range_hz(vsys, vwidth)
	inds = (((freq_axis-half_chan) >= low_freq_hz) *
		((freq_axis+half_chan) <= high_freq_hz))
	mask_axis[inds] = True
	vel_inds = MW_indices(freq_axis)
	mask_axis[vel_inds] = True

	regions = (label(mask_axis))[0]
	max_reg = np.max(regions)
	for ii in range(1, max_reg+1):
		this_mask = (regions == ii)
		low_chan = np.min(chan_axis[this_mask])
		high_chan = np.max(chan_axis[this_mask])
		this_spw_string = str(low_chan)+'~'+str(high_chan)
		if first_string:
			spw_flagging_string += this_spw_string
			first_string = False
		else:
			spw_flagging_string += ','+this_spw_string
	return spw_flagging_string

## parse name of visibiltiy from input path
msName = args.msPath

## parse velocities
vsys = args.v_sys
vwidth = args.vwidth
def main():
	fitspwStr = '0:'
	chan_str = construct_spw_str(vsys, vwidth)
	fitspwStr += chan_str
	statwt_params = {
		'vis': msName,
		'fitspw': fitspwStr,
		'excludechans': True,
		'timebin': '0.001s'}
	statwt(**statwt_params)
if __name__=='__main__':
	main()
	exit()
