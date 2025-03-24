import argparse

## parse user arguments
def parse_user_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help = '<required> name of casa image', required = True)
    parser.add_argument('-r', '--region', help = '<required> name of CASA region file', required = True)
    args, unknown = parser.parse_known_args()
    return args.name, args.region

def run_imsubimage(f_name, region_name):
    imsub_params = {
            'imagename': f_name,
            'outfile':'%s.imsub' % f_name,
            'region': region_name
            }
    imsubimage(**imsub_params)
    return
def main():
    f_name, region_name = parse_user_arguments()
    run_imsubimage(f_name, region_name)
if __name__=='__main__':
    main()
    exit()