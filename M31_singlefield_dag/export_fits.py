import argparse

## parse user arguments
def parse_user_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help = '<required> name of casa image', required = True)
    parser.add_argument('-e', '--extension', help = '<required> extension', required = True)
    args, unknown = parser.parse_known_args()
    return args.name, args.extension

def run_export_fits(f_name, extension):
    export_fits_params = {
            'imagename':'%s.%s' % (f_name, extension),
            'fitsimage':'%s.%s.fits' % (f_name, extension),
            'velocity':True
            }
    exportfits(**export_fits_params)
    return
def main():
    f_name, extension = parse_user_arguments()
    run_export_fits(f_name, extension)
if __name__=='__main__':
    main()
    exit()
