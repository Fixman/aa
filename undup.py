from __future__ import print_function

import pandas
import numpy
import sys

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description = 'Removes duplicated columns in a DataFrame')
    parser.add_argument('df', help = 'csv file to deduplicate.')
    return parser.parse_args()

def main():
    args = parse_args()

    columns = pandas.read_csv(args.df, nrows = 0).columns
    duplicated = numpy.ones_like(columns, dtype = bool)

    sys.setrecursionlimit(10000)
    for e, c in enumerate(pandas.read_csv(args.df, chunksize = 10000)):
        duplicated &= c.T.duplicated().T

    print('Removing {} duplicated columns.'.format(duplicated.sum()), file = sys.stderr)

    dedup_columns = columns[~duplicated]

    first = True
    for c in pandas.read_csv(args.df, chunksize = 10000):
        c[dedup_columns].to_csv(sys.stdout, header = first, index = False)
        first = False

if __name__ == '__main__':
    main()
