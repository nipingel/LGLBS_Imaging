"""
04/19/2023
concatenate input measurement sets into a single file
User inputs:
-p --path - path to measurement sets
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
"""
# imports
import argparse
import glob as glob

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help = '<required> path to measurement sets', required = True)
args, unknown = parser.parse_known_args()

## parse measurement set list & output
path = args.path

## make list of measurement sets
def make_list(path, ext):
	ms_list = glob.glob('%s/*%s' % (path, ext))
	return ms_list

## run concat
def run_concat(ms_list, output_vis):
	concat_params = {
		'vis': ms_list,
		'concatvis':output_vis,
		'freqtol':'0.4kHz',
		'dirtol': '0.1deg'}
	concat(**params)

def main():
	## get list of input measurement sets
	ms_list_field14 = make_list(path, '*_14.transformed.contsub')
	ms_list_field47 = make_list(path, '*_47.transformed.contsub')
	output_vis_field14 = '%s/M31_field14.ms' % path
	output_vis_field47 = '%s/M31_field47.ms' % path
	## run task
	run_concat(ms_list_field14, output_vis_field14)
	run_concat(ms_list_field47, output_vis_field47)
if __name__=='__main__':
	main()
	exit()
