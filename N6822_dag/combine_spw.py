"""
4/3/2023
run CASA task mstransform to combine spectral windows of a concatenated measurement set
User inputs:
-p --path - <required> path of input ms file
-n --name - <required> input name of ms file
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source_name', help = '<required> name of source, required = True')
parser.add_argument('-n', '--name', help='<required> name of input measurement set', required = True)
args, unknown = parser.parse_known_args()

## parse measurement set list & output
src_name = args.src_name
input_name = args.name

## construct list of ms files to be concatenated
ms_path = '/projects/vla-processing/measurement_sets/%s/%s' % (src_name, input_name)
output_vis = ms_path.replace('.ms', '_combined_spw.ms')

def main():
	mstransform(vis = ms_path, outputvis = output_vis, datacolumn = 'data', combinespws = True)
if __name__=='__main__':
	main()
	exit()
