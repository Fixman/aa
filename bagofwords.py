from __future__ import print_function
from __future__ import division

import pandas
import sys

from argparse import ArgumentParser
from sklearn.frature_extraction.text import CountVectorizer

def parse_args():
    parser = ArgumentParser(
        description = 'Tells which emails contain certain words',
    )
    parser.add_argument('subject_word_file', type = file, help = 'File with words for the subject.')
    parser.add_argument('body_word_file', type = file, help = 'File with words for the body.')
    args = parser.parse_args()

    args.subject_words = map(str.strip, args.subject_word_file.readlines())
    args.body_words = map(str.strip, args.body_word_file.readlines())

    return args

def main():
    args = parse_args()

    features = pandas.read_csv(sys.stdin, usecols = ['num', 'subject', 'body'], index_col = 'num', dtype = object)

    df = pandas.DataFrame(index = features.index)

    for w in args.subject_words:
        df['subject_contains_' + w] = features.subject.str.contains(w, case = False)
        print('Subject: ' + w, file = sys.stderr)

    for w in args.body_words:
        df['body_contains_' + w] = features.body.str.contains(w, case = False)
        print('Body: ' + w, file = sys.stderr)

    df.to_csv(sys.stdout, index = True, header = True)

if __name__ == '__main__':
    main()
