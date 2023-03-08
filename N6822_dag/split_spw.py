"""
10/3/2022
Split out a user provided spectral window from a measurement set
User inputs:
-p --path - <required> path of ms file
-v --vsys -  <required> systematic velocity (assumed LSRK)'
-w --vwidth - <required> velocity width
-r --restfreq - <required> rest freq (assumed GHz)
-s --source_name - <required> source name (used to select science scans)
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
parser.add_argument('-s', '--source_name', help='<required> source name (used to select science scans)', required = True)
args, unknown = parser.parse_known_args()

## get path to measurement set
ms_path = args.path

## parse velocity parameters
vsys = args.vsys
vwidth = args.vwidth
rest_freq = args.rest_freq

## get source name
src_name = args.source_name

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
def main():
	vis_name = ms_path
	output_vis = '%s_spw' % (ms_path)
	src_str = '%s*' % (src_name)
	timebin_str = '5s'
	datacolumn_name = 'data'
	split(vis = vis_name, outputvis = output_vis, spw=spw_val, datacolumn=datacolumn_name, field=src_str, timebin = timebin_str)
if __name__=='__main__':
	main()
	exit()
