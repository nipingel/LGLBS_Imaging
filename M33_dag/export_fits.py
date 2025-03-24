import argparse

## parse user arguments
def parse_user_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help = '<required> name of casa image', required = True)
    args, unknown = parser.parse_known_args()
    return args.name

def run_export_fits(f_name):
    export_fits_params = {
            'imagename':'%s' % (f_name),
            'fitsimage':'%s.fits' % (f_name),
            'velocity':True,
            'dropdeg': True,
            'dropstokes': True
            }
    exportfits(**export_fits_params)
    return
def main():
    f_name = parse_user_arguments()
    run_export_fits(f_name)
if __name__=='__main__':
    main()
    exit()