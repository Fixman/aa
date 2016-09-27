from __future__ import division
from __future__ import print_function

import numpy
import pandas
import sys

from argparse import ArgumentParser
from sklearn.feature_extraction import DictVectorizer

def parse_args():
    parser = ArgumentParser(
        description = 'Do OneHotEncoding to some columns of a CSV file with mail data.',
    )
    parser.add_argument('-c', '--column_file', required = True, type = file, help = 'File with final column list.')
    args = parser.parse_args()

    args.columns = pandas.Index(map(str.strip, args.column_file.readlines()))

    return args

def main():
    args = parse_args()
    
    cols = args.columns.str.partition('=').levels[0] | ['num']
    table = pandas.read_csv('data/train.csv', usecols = cols, index_col = 'num', dtype = object)
    
    dv = DictVectorizer(sparse = False)
    transformed = dv.fit_transform(table.apply(lambda x: x.str.strip()).to_dict(orient = 'records'))
    df = pandas.DataFrame(transformed, columns = dv.get_feature_names(), index = table.index)

    res = df.reindex(columns = args.columns, fill_value = 0).astype(int)
    res.to_csv(sys.stdout, index = True, header = True)

    print('Features without any hit: {}'.format(', '.join(res.columns[(res == 0).all(axis = 0)])), file = sys.stderr)

if __name__ == '__main__':
    main()
