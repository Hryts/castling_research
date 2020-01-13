import os
import glob
import parser


if __name__ == '__main__':
    print('decompressing files...')
    os.system('mv ~/Downloads/fics* ./data')
    os.system('bzip2 -d data/*.bz2')
    print('parsing files...')
    for filename in glob.glob('./data/fics*'):
        res_filename = 'csv_data/' + filename.split(sep='_')[1] + '.csv'
        parser.parse(filename, res_filename, -1)
