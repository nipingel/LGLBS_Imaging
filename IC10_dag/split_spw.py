"""
05/03/2023
Split out a user provided spectral window from a measurement set
User inputs:
-p --path - <required> path of ms file
-v --vsys -  <required> systematic velocity (assumed LSRK)'
-w --vwidth - <required> velocity width
-r --restfreq - <required> rest freq (assumed GHz)
-5 --time_bin - <required> time over which to average visibilities in units of sec (e.g., 5)
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse
from phangsPipeline import casaVisRoutines as cvr

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help = '<required> path to measurement set', required = True)
parser.add_argument('-v', '--vsys', help='<required> systematic velocity (assumed LSRK)', type = int, required = True)
parser.add_argument('-w', '--vwidth', help='<required> velocity width', type = int, required = True)
parser.add_argument('-r', '--rest_freq', help='<required> rest frequency (assumed GHz)', type=float, required = True)
parser.add_argument('-t', '--time_bin', help='<required> time over which to average visibilities in units of sec (e.g., 5)', required = True)
args, unknown = parser.parse_known_args()

## get path to measurement set
ms_path = args.path

## parse velocity parameters
vsys = args.vsys
vwidth = args.vwidth
rest_freq = args.rest_freq
time_bin_value = args.time_bin

def main():
	## get possible science spws
	spw_science = cvr.find_spws_for_science(infile = ms_path)

	## get intended line based on input systemic velocity, width, & rest frequency
	spw_lines = cvr.find_spws_for_line(infile = ms_path, vsys_kms=vsys, vwidth_kms=vwidth, restfreq_ghz=rest_freq) 

	if len(spw_lines) > 1:
		## split up by commas
		spw_science_split = spw_science.split(',')
		spw_lines_split = spw_lines.split(',')
		## extract overlappying elements in splitted array
		spw_val = list(set(spw_science_split).intersection(spw_lines_split))[0]
	else:
		spw_val = spw_lines

	## construct parameter dictionary
	output_vis = '%s_spw' % (ms_path)
	timebin_str = '%ss' % (time_bin_value)
	intent_str = 'OBSERVE_TARGET*'
	split_params = {
		'vis': ms_path,
		'outputvis': output_vis, 
		'spw': spw_val,
		'intent': intent_str,
		'timebin': timebin_str,
		'datacolumn': 'data'
	}
	split(**split_params)
if __name__=='__main__':
	main()
	exit()