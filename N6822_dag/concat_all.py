"""
03/20/2023
concatenate input measurement sets into a single file
User inputs:
-s --src_name - <required> name of souce
-o --output_name - <required> name of output concatentated measurement set
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
parser.add_argument('-s', '--src_name', help='<required> name of souce', required = True)
parser.add_argument('-o', '--output', help='<required> name of output concatentated measurement set', required = True)
args, unknown = parser.parse_known_args()

## parse measurement set list & output
src_name = args.src_name
output_vis = args.output

## construct list of ms files to be concatenated
ms_list = glob.glob('/projects/vla-processing/measurement_sets/%s/*.split_concat' % src_name)
output_name = '/projects/vla-processing/measurement_sets/%s/%s' % (src_name, output_vis)
print(ms_list)
print(output_name)
def main():
	concat_params = {
		'vis': ms_list,
		'concatvis':output_name,
		'freqtol':'0.4kHz',
		'dirtol': '0.1deg'}
	concat(**concat_params)
if __name__=='__main__':
	main()
	exit()
