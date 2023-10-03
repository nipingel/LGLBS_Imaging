"""
04/02/2023
script to build an input text file for an additional run of splitting off non-overlappying channels
to ensure all measurement sets can be concatenated together. Columns of output text file:
name of measurement set, starting channel to split, ending channel to split

User inputs:
-p --path - path to directory containing measurement sets
-e --extension - file extension for generated list of input measurement sets
-o --output - output name of text file
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""

# imports
import argparse
import sys
import os
import glob as glob
import csv
sys.path.append('/home/nmpingel/software/analysis_scripts')
import numpy as np 
import analysisUtils as au

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help = '<required> path to directory containing measurement sets', required = True)
parser.add_argument('-e', '--extension', help = '<required> file extension for generated list of input measurement sets', required = True)
parser.add_argument('-o', '--output', help='<required> output name of text file', required = True)
args, unknown = parser.parse_known_args()

## function to build lists of necessary spw info
def build_lists(file_list):
	## define lists to store required info
	tot_chans_list = []
	freq_chans_list = []

	## initial loop to build lists
	for ms_file in file_list:
		vm = au.ValueMapping(ms_file)

		## get dictionary of spectral window info
		spw_dict = vm.spwInfo[0]

		## fill lists
		tot_chans_list.append(spw_dict['numChannels'])
		freq_chans_list.append(spw_dict['chanFreqs'])
	return tot_chans_list, freq_chans_list

## function to pull out measurement sets that have different number of total channels 
## than the minimum number
def parse_lists(ms_list, tot_chans_list, freq_chan_list, ext):
	min_total_chans = np.min(tot_chans_list)
	## get indices of measurement set list that exceed minimum number of channels
	bad_idxs = np.where(np.array(tot_chans_list) > min_total_chans)

	## find one instance of ms file with minimum number of total channels to return
	good_idxs = np.where(np.array(tot_chans_list) == min_total_chans)

	## extract name of measurement sets and associated freq_chans using returned bad indices
	extracted_ms_list = [ms_list[i] for i in bad_idxs[0]]
	extracted_freq_chan_list = [freq_chan_list[i] for i in bad_idxs[0]]
	## extract one instance of freq_chans from measurement set that has minimum number of total channels
	extracted_min_freq_chan_list = [freq_chan_list[i] for i in good_idxs[0]]
	extracted_min_ms_list = [ms_list[i] for i in good_idxs[0]]

	## append 'split_concat' file extension so subsequent concat can capture all measurement sets
	for old_name in extracted_min_ms_list:
		new_name = old_name.replace(ext, 'contsub.split_concat')
		os.rename(old_name, new_name)
	## account for instance where extracted_min_freq_chan_list is only a single element
	if len(extracted_min_freq_chan_list) > 1:
		return extracted_ms_list, extracted_freq_chan_list, extracted_min_freq_chan_list[0]
	else:
		return extracted_ms_list, extracted_freq_chan_list, extracted_min_freq_chan_list

## function to determine first and last channels to be split out from measurement sets with greater number of channels 
def define_start_and_end_channels(min_freq_chans, freq_chan_list):
	## loop through list of extracted channels
	min_low_edge = np.min(min_freq_chans)
	min_high_edge = np.max(min_freq_chans)
	## define lists to store start/end channels for split
	start_chan_list = []
	end_chan_list = []
	for freq_chans in freq_chan_list:
		#mask_axis = np.zeros_like(freq_chans, dtype='bool')
		mask_axis = (freq_chans >= min_low_edge)*(freq_chans <= min_high_edge)
		true_inds = np.where(mask_axis == True)
		start_chan_list.append(true_inds[0][0])
		end_chan_list.append(true_inds[0][-1]+1)
	return start_chan_list, end_chan_list

## function to write name of measurement set, starting chan, and ending chan as a row in output text file
def write_to_file(ms_list, s_list, e_list, output):
	with open('%s.csv' % output, 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=",")
		for i in range(0, len(ms_list)):
			row = []
			row.append(ms_list[i])
			row.append(s_list[i])
			row.append(e_list[i])
			writer.writerow(row)
	csvfile.close()

## parse user arguments
ms_path = args.path
file_ext = args.extension
output_name = args.output

def main():

	## collect names of measurement sets to be checked
	ms_list = glob.glob('%s/*.%s' % (ms_path, file_ext))

	## build lists from spw info
	total_channels_list, freq_channels_list = build_lists(ms_list)

	## parse lists to find ms files with total channels that exceed the minimum
	extracted_ms_list, extracted_freq_chan_list, min_freq_chans = parse_lists(ms_list, total_channels_list, freq_channels_list, file_ext)

	## get lists of starting and ending channels for splitting
	start_chan_list, end_chan_list = define_start_and_end_channels(min_freq_chans, extracted_freq_chan_list)

	## finally, write name of measurement sets, starting, and ending channels to comma-separated text file
	write_to_file(extracted_ms_list, start_chan_list, end_chan_list, output_name)

if __name__=='__main__':
	main()
	exit()
