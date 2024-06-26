"""
5/4/2023
Split out a user provided channel range from input ms file
User inputs:
-p --path - <required> path of ms file
-s --start_chan - <required> starting channel for splitting
-e --end_chan - <required> ending channel for splliting
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
parser.add_argument('-s', '--start_chan', help='<required> starting channel for splitting', required = True, type = int)
parser.add_argument('-e', '--end_chan', help='<required> ending channel for splitting', required = True, type = int)
parser.add_argument('--split_concat', action='store_true')
parser.add_argument('--indv_channel', dest='split_concat', action='store_false')
parser.set_defaults(for_concat=True)

args, unknown = parser.parse_known_args()

## get path to measurement set
ms_path = args.path

## get starting and ending channels
start_chan = args.start_chan
end_chan = args.end_chan

## are we splitting for concat or individual channels for imaging?
split_concat = args.split_concat

def main():
	if split_concat:
		split_params = {
		'vis': ms_path,
		'outputvis': '%s.split_concat' % ms_path,
		'spw': '0:%d~%d' % (start_chan, end_chan),
		'datacolumn': 'data'
		}
		split(**split_params)
	else:
		## create list of file names
		output_vis_list = []
		for i in range(start_chan, end_chan):
			output_vis_list.append('%s_chan%d' % (ms_path, i))

		cnt = 0
		for i in range(start_chan, end_chan):
			split_params = {
			'vis': ms_path,
			'outputvis': output_vis_list[cnt],
			'spw': '0:%d' % i,
			'datacolumn': 'data'
			}

			## set split parameters and run
			vis_name = ms_path
			output_vis = output_vis_list[cnt]
			spw_str='0:%d' % i
			datacolumn_name = 'data'
			cnt+=1
			split(**split_params)
if __name__=='__main__':
	main()
	exit()