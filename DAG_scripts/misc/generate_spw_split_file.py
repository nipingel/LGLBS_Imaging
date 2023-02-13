"""
02/13/2023
read contents of directory and construct file used as input to split_spw tasks in LGLBS DAG
User inputs:
-p --path - <required> path to directory containing ms files
-o --output - <required> name of output text file
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
parser.add_argument('-p', '--path', help = '<required> path to directory containing ms files', required = True)
parser.add_argument('-o', '--output', help='<required> name of output text file', required = True)
args, unknown = parser.parse_known_args()

## get user arguments 
data_dir = args.path
output_name = args.output

## get list of input files
input_list = glob.glob('%s/*.tar' % data_dir)

f = open('%s.txt' % output_name, "w")
for f_name in input_list:
	full_name = f_name.split('/')[-1]
	name_array = full_name.split('_')
	f.write('%s, %s_%s' % (full_name, name_array[0], name_array[1]))
	f.write('\n')
f.close()
