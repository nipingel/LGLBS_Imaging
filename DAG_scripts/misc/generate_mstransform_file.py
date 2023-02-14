"""
02/13/2023
read contents of directory and construct file used as input to ms_transform tasks in LGLBS DAG
User inputs:
-p --path - <required> path to directory containing ms files
-s --spw - <required> spectral window string
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
parser.add_argument('-s', '--spw', help = '<required> spw string (e.g., 5)', required = True)
parser.add_argument('-o', '--output', help='<required> name of output text file', required = True)
args, unknown = parser.parse_known_args()

## get user arguments 
data_dir = args.path
output_name = args.output
spw_str = args.spw

## get list of input files
input_list = glob.glob('%s/*.tar' % data_dir)

f = open('%s.txt' % output_name, "w")
for f_name in input_list:
	full_name = f_name.split('/')[-1]
	name_array = full_name.split('_')
	split_dot_name = name_array[-1].split('.')
	f.write('%s.%s.%s.%s.%s.%s.%s.%s_spw%s.tar' % (split_dot_name[0], split_dot_name[1], split_dot_name[2], split_dot_name[3], split_dot_name[4], split_dot_name[5], split_dot_name[6], split_dot_name[7], spw_str))
	f.write('\n')
f.close()
