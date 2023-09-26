"""
04/19/2023
combine spectral windows in concatenated measurement set
User inputs:
-p --path - path to measurement sets
-n --input_name - name of input measurement set
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
parser.add_argument('-p', '--path', help = '<required> path to measurement set', required = True)
parser.add_argument('-n', '--input_name', help = '<required> name of input measurement set', required = True)
args, unknown = parser.parse_known_args()

## parse measurement set list & output
path = args.path
input_name = args.input_name

def main():
	## get list of input measurement sets
	full_input_name = '%s/%s' % (path, input_name)
	output_vis = '%s/%s' % (path, input_name.replace('.ms', '.comb_spw'))
	mstransform_params = {
		'vis': full_input_name,
		'outputvis': output_vis,
		'datacolumn': 'data',
		'combinespws': True
	}
	mstransform(**mstransform_params)
if __name__=='__main__':
	main()
	exit()