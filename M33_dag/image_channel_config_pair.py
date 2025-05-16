"""
5/16/2025
Image configuration pair in a single channel---assumed VLA
User inputs:
-v --vis_path - <required> path of ms file
-r --ra - <required> ra phase center in form e.g.: 00h40m13.8 
-d --dec - <required> dec phase center in form e.g.: +40d50m04.73
-o --output_name - <required> name of output file
-p --config_pair - <required> configuration pair (e.g, A+B)
__author__="Nickolas Pingel"
__version__="1.0"
__email__="nmpingel@wisc.edu"
__status__="Production"
"""
# imports
import argparse

## parse user inputs
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vis_path', help = '<required> name of measurement set', required = True)
parser.add_argument('-r', '--ra', help = '<required> ra phase center in form e.g.: 00h40m13.8', required = True)
parser.add_argument('-d', '--dec', help = '<required> ra phase center in form e.g.: +40d50m04.73', required = True)
parser.add_argument('-o', '--output_name', help = '<required> name of output file', required = True)
parser.add_argument('-p', '--config_pair', help = '<required> configuration pair (e.g, A+B)', required = True)
args, unknown = parser.parse_known_args()

vis_path = args.vis_path
ra_phase_center = args.ra
dec_phase_center = args.dec
output_name = args.output_name
config_pair = args.config_pair

## TODO:
A+C
A+D
B+C
B+D
C+D

## dictionary between config pair and min/max baselines
config_pair_dict = 
	{'A+B':'0.68~',
	{'A+C': }
	}

def main():
	#casalog.filter('DEBUG2')   
	## define tclean variables below
	## image output properties
	im_size = 8500
	field_id = 'M33*'
	cell_size = '0.75arcsec'
	restore_beam = 'common'
	use_mask = 'pb'
	
	## deconvolution parameters
	deconvolver_mode = 'multiscale'
	ms_scales = [0, 8, 16, 32, 64, 128, 256]
	tot_niter = 0
	min_threshold = '0.8mJy'
	restart_parameter = False
	## tclean dictionary
	tclean_params={
		'vis':vis_path,
		'imagename':output_name,
		'phasecenter':'J2000 %s %s' % (ra_phase_center, dec_phase_center),
		'restfreq':'1.42040571183GHz',
		'selectdata': True,
		'field': field_id,
		'datacolumn': 'data',
		'specmode':'mfs',
		'imsize':im_size,
		'cell':cell_size,
		'restoringbeam': restore_beam, 
		'pblimit':0.1, 
		'weighting':'briggs', 
		'robust':1.0, 
		'gridder':'wproject', 
		'pbcor':True, 
		'niter':tot_niter, 
		'deconvolver':deconvolver_mode, 
		'scales':ms_scales, 
		'smallscalebias':0.4, 
		'cyclefactor':0.8, 
		'minpsffraction':0.05, 
		'maxpsffraction':0.8, 
		'threshold':min_threshold, 
		'usemask':use_mask, 
		'pbmask':0.2, 
        'parallel':True,
		'restart':restart_parameter
		}

	## run tclean
	tclean(**tclean_params)
if __name__=='__main__':
	main()
	exit()
