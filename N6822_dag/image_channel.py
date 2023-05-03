"""
8/29/2022
Image LGLBS source around user provided phase center
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
parser.add_argument('-v', '--vis_path', help = '<required> name of measurement set', required = True)
#parser.add_argument('-p', '--phase_center', help = '<required> phase center in form e.g.: J2000 00h40m13.8 +40d50m04.73', required = True)
#parser.add_argument('-s', '--start_chan', help = '<required> start channel to split from main measurement set', required = True, type = int)
parser.add_argument('-o', '--output_name', help = '<required> name of output file', required = True)
args, unknown = parser.parse_known_args()

vis_path = args.vis_path
#phase_center = args.phase_center
#start_chan = args.start_chan
output_name = 'NGC6822_A+B+C+D_combined_spw.ms_chan770_dirty'

def main():
	phasecenter='J2000 19h44m57.74s -14d48m12.4'
	rest_freq='1.42040571183GHz'
	#output_name='wlm_center'
	#vis_name='imaging/wlmctr/wlmctr_B+C+D_hi21cm.ms'
	vis_name= 'NGC6822_A+B+C+D_combined_spw.ms_chan770'
	## output image properties
	restore_beam = 'common'
	cell_size = '0.75arcsec'
	im_size = 8192
	## automasking parameters ##
	use_mask = 'pb'
	#use_mask = 'auto-multithresh'
	sidelobe_threshold = 2.5
	noise_threshold = 3.5
	min_beam_frac = 0.3
	lownoisethreshold = 1.5
	negativethreshold = 0.0
	grow_iters=75
	dogrowprune=False
	verbose = True
	## deconvolution parameters
	deconvolver_mode = 'multiscale'
	ms_scales = [0, 8, 16, 32, 64, 128, 256, 512, 1024]
	#ms_scales = [64, 128, 256, 512]
	tot_niter = 0
	min_threshold = '2.175mJy'
	restart_parameter = False
	tclean(vis=vis_path, imagename=output_name, selectdata = True, datacolumn = 'data', restfreq=rest_freq, specmode = 'mfs', phasecenter=phasecenter,imsize=im_size, 
		cell=cell_size, restoringbeam=restore_beam, pblimit = 0.1,  weighting='briggs', robust = 1.0, gridder='wproject', pbcor=True, niter=tot_niter, deconvolver = deconvolver_mode, 
		scales = ms_scales, smallscalebias = 0.4, cyclefactor = 0.8, minpsffraction=0.05, maxpsffraction = 0.8, threshold = min_threshold, usemask = use_mask, pbmask = 0.5, 
		sidelobethreshold = sidelobe_threshold, noisethreshold = noise_threshold, minbeamfrac = min_beam_frac, lownoisethreshold = lownoisethreshold, negativethreshold = 0.0, growiterations = grow_iters, 
		dogrowprune = False, verbose = True, restart = restart_parameter)
if __name__=='__main__':
	main()
	exit()
	
