from __future__ import print_function
from __future__ import division

import pandas
import sys

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(
        description = 'Joins some DataFrames by the first column.'
    )
    parser.add_argument('dataframes', nargs = '*', help = 'Dataframes to join')
    return parser.parse_args()

def main():
    args = parse_args()

    k = pandas.read_csv(args.dataframes[0], index_col = 0)
    for p in args.dataframes[1:]:
        k = k.merge(pandas.read_csv(p, index_col = 0), left_index = True, right_index = True)

    k.to_csv(sys.stdout, index = True, header = True)

if __name__ == '__main__':
    main()
