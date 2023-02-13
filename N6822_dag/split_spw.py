"""
10/3/2022
Split out a user provided spectral window from a measurement set
User inputs:
-p --path - <required> path of ms file
-s --spw - <required> spw
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help = '<required> path to measurement set', required = True)
parser.add_argument('-s', '--spw', help='<required> spw', required = True)
args, unknown = parser.parse_known_args()

## get path to measurement set
ms_path = args.path

## get starting and ending channels
spw_val = args.spw
def main():
	vis_name = ms_path
	output_vis = '%s_spw%s' % (ms_path, spw_val)
	intent_str = 'OBSERVE_TARGET*'
	timebin_str = '5s'
	datacolumn_name = 'data'
	split(vis = vis_name, outputvis = output_vis, spw=spw_val, datacolumn=datacolumn_name, intent = intent_str, timebin = timebin_str)
if __name__=='__main__':
	main()
	exit()
