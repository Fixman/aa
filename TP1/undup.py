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

    columns = pandas.read_csv(args.df, nrows = 0, index_col = 'num').columns
    duplicated = numpy.ones_like(columns, dtype = bool)
    fun = numpy.zeros_like(columns, dtype = bool)

    sys.setrecursionlimit(10000)
    for e, c in enumerate(pandas.read_csv(args.df, chunksize = 10000, index_col = 'num')):
        duplicated &= c.T.duplicated().T
        fun |= c.apply(lambda x: pandas.concat([x.value_counts(sort = True, normalize = True), pandas.Series([0])]).iloc[1] >= .005)

    print('Removing {} duplicated and keeping {} fun columns.'.format(duplicated.sum(), fun.sum()), file = sys.stderr)

    dedup_columns = columns[~duplicated & fun]

    first = True
    for c in pandas.read_csv(args.df, chunksize = 10000, index_col = 'num'):
        c[dedup_columns].to_csv(sys.stdout, header = first, index = True)
        first = False

if __name__ == '__main__':
    main()
