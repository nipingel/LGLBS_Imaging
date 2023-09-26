"""
04/19/2023
concatenate input measurement sets into a single file
User inputs:
-o --output_name - name of output concatentated measurement set
-p --path - path to measurement sets
-e --extension - file extension to use to create list of input measurement sets
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse
import glob as glob

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='<required> name of output concatentated measurement set', required = True)
parser.add_argument('-p', '--path', help = '<required> path to measurement sets', required = True)
parser.add_argument('-e', '--extension', help = '<required> file extension to use to create list of input measurement sets', required = True)
args, unknown = parser.parse_known_args()

## parse measurement set list & output
output_name = args.output
path = args.path
ext = args.extension

def main():
	## get list of input measurement sets
	ms_list = glob.glob('%s/*.%s' % (path, ext))
	output_vis = '%s/%s' % (path, output_name)
	concat_params = {
		'vis': ms_list,
		'concatvis':output_vis,
		'freqtol':'0.4kHz',
		'dirtol': '0.1deg'}
	concat(**concat_params)
if __name__=='__main__':
	main()
	exit()