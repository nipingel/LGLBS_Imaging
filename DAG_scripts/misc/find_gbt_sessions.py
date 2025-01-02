"""
04/30/2024
Print out observing sessions for user-provided source name and GBO project
User inputs:
-p --project - <required> path of ms file
-s --source -  <required> systematic velocity (assumed LSRK)'
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""

# imports
import argparse
import glob
from astropy.io import fits

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--project', help = '<required> name of GBO project (e.g., AGBT23B_162)', required = True)
parser.add_argument('-s', '--source', help='<required> name of source', required = True)
args, unknown = parser.parse_known_args()

## get user inputs
project_name = args.project
source_name = args.source

## set data directory
data_dir = '/home/archive/science-data'

def main():
	## parse project to get observing semester
	obs_semester = project_name.split('AGBT')[-1][0:3]

	## read in list of sessions 
	sessions = glob.glob('%s/%s/%s*' % (data_dir, obs_semester, project_name))

	## loop through sessions to check if our source was observed
	for session in sessions:
		scans = glob.glob(session+'/Antenna/*.fits')
		for scan in scans:
			hdu = fits.open(scan)
			object_name = hdu[0].header['OBJECT']
			if object_name == source_name:
				print('Source %s observed in %s' % (source_name, session))
				break

if __name__=='__main__':
	main()
	exit()
