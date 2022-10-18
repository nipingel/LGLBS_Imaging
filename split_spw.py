"""
10/3/2022
Split out a user provided spectral window from a measurement set
User inputs:
-p --path - <required> path of ms file
-s --start_chan - <required> starting channel for splitting
-e --end_chan - <required> ending channel for splliting
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
	output_vis = '%s_spw%d' % (ms_path, spw_val)
	intent_str = 'OBSERVE_TARGET*'
	spw_str='0:%s' % i
	timebin_str = '20s'
	datacolumn_name = 'data'
	split(vis = vis_name, outputvis = output_vis, spw=spw_str, datacolumn=datacolumn_name, intent = intent_str, timebin = timebin_str)
if __name__=='__main__':
	main()
	exit()
