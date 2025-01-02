"""
11/4/2022
run CASA task mstransform to regrid channel width and output spectral reference frame to match staged BCD measurement sets
User inputs:
-p --path - <required> path of ms file
-w --channel_width - <required> channel width in kHz
-f --frame - <required> output spectral reference frame
-o --output_vis - <required> name of transformed visibility
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
parser.add_argument('-w', '--channel_width', help='<required> channel width in kHz', required = True)
parser.add_argument('-f', '--frame', help='<required> output spectral reference frame', required = True)
parser.add_argument('-o', '--output_vis', help='<required> name of transformed visibility', required = True)
args, unknown = parser.parse_known_args()

## get path to measurement set
ms_path = args.path

## get channel width
channel_width = args.channel_width
channel_width += 'Hz'

## get output reference frame
ref_frame =  args.frame

## get transformed visibility name
output_vis = args.output_vis

def main():
	mstransform_params = {
		'vis': ms_path,
		'outputvis': output_vis,
		'datacolumn': 'data',
		'regridms': True, 
		'mode': 'frequency',
		'width': channel_width,
		'outframe': ref_frame
	}
	mstransform(**mstransform_params)
if __name__=='__main__':
	main()
	exit()