"""
5/04/2023
Image LGLBS source around user provided phase center
User inputs:
-v --vis_path - <required> path of ms file
-r --ra - <required> ra phase center in form e.g.: 00h40m13.8 
-d --dec - <required> dec phase center in form e.g.: +40d50m04.73
-p --output_name - <required> name of output file
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
args, unknown = parser.parse_known_args()

vis_path = args.vis_path
ra_phase_center = args.ra
dec_phase_center = args.dec
output_name = args.output_name

def main():
    #casalog.filter('DEBUG2')   
    ## define tclean variables below
    ## image output properties
    im_size = 8500
    field_id = 'M33*'
    cell_size = '0.75arcsec'
    restore_beam = 'common'
    ## automasking parameters ##
    use_mask = 'pb'
    mask = 'M33_A+B+C+D.wt_flagged_chan830.mask'
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
    ms_scales = [0, 8, 16, 32, 64, 128, 256]
    tot_niter = 100000 
    #min_threshold = '1.35mJy'
    min_threshold = '0.6mJy'
    restart_parameter = False
    ## tclean dictionary
    tclean_params={
        'vis':vis_path,
        'imagename':output_name,
        'phasecenter':'J2000 %s %s' % (ra_phase_center, dec_phase_center),
        'restfreq':'1.42040571183GHz',
        'selectdata': True,
        'field': field_id,
        'spw': '0:0',
        'datacolumn': 'data',
        'specmode':'mfs',
        'imsize':im_size,
        'cell':cell_size,
        'restoringbeam': restore_beam, 
        'pblimit':0.2, 
        'weighting':'briggs', 
        'robust':1.0, 
        'gridder':'mosaic',
        'mosweight':False,
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
        'sidelobethreshold':sidelobe_threshold, 
        'noisethreshold':noise_threshold, 
        'minbeamfrac':min_beam_frac, 
        'lownoisethreshold':lownoisethreshold, 
        'negativethreshold':0.0, 
        'growiterations':grow_iters, 
        'dogrowprune':False, 
        'verbose':True,
        'parallel':True,
        'restart':restart_parameter
        }

    ## run tclean
    tclean(**tclean_params)
if __name__=='__main__':
    main()
    exit()
