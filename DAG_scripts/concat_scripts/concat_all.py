"""
11/14/2i022
concatenate input measurement sets into a single file
User inputs:
-l --ms_list - list of measurement sets to concatentate
-o --output_name - name of output concatentated measurement set
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--ms_list', nargs = '+', help='<required> list of measurement sets to concatentate', required = True)
parser.add_argument('-o', '--output', help='<required> name of output concatentated measurement set', required = True)
args, unknown = parser.parse_known_args()

## parse measurement set list & output
ms_list = args.ms_list
output_vis = args.output

def main():
	concat_params = {
		'vis': ms_list,
		'concatvis':output_vis,
		'freqtol':'0.4kHz',
		'dirtol': '0.1deg'}
	concat(**concat_params)
if __name__=='__main__':
	main()
	exit()
