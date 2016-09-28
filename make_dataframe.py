from __future__ import print_function

import json
import pandas
import sys

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(
        description = 'Parses ham and spam JSON files and prints them in DataFrame format.',
        epilog = 'This is done the lazy way to it uses a lot of memory.'
    )
    parser.add_argument('--only', action = 'store_true', help = 'Parse only one file.')
    parser.add_argument('ham', type = file, help = 'JSON file with ham (ham_train.json).')
    parser.add_argument('spam', type = file, nargs = '?', help = 'JSON file with spam (spam_train.json).')
    return parser.parse_args()

def getlinesep(mail):
    lineseps = ['\r\n', '\n']
    return next(x for x in lineseps if 2 * x in mail)

def parse(mail):
    ls = getlinesep(mail)
    bs = 2 * ls
    
    header, body = mail.split(bs, 1)
    header = header.replace(ls + '\t', ' ').replace(ls + ' ', ' ')
    
    header = [(str(x).replace('_', '--'), y) for x, y in [z.split(':', 1) for z in header.split(ls)]]
    body = ('body', body)

    result = header + [body] + [('my_linesep', ls)]
    result = [(k, v.replace('\n', '<NL>').replace('\r', '<CR>')) for k, v in result]
    
    return result

def try_parse(mail):
    try:
        return parse(mail)
    except ValueError:
        return {'my_unparseable': True, 'my_reason': 'badheader'}
    except StopIteration:
        return {'my_unparseable': True, 'my_reason': 'nosep'}

def parse_file(f):
    raw = json.load(f)
    msg = map(try_parse, raw)
    print('{}/{} unparseable messages in {}'.format(len([x for x in msg if 'unparseable' in x]), len(raw), f.name), file = sys.stderr)

    return pandas.DataFrame(map(dict, msg))

def main():
    args = parse_args()

    ham = parse_file(args.ham)
    spam = None
    if not args.only:
        spam = parse_file(args.spam)
        spam['spam'] = True
        ham['spam'] = False

    pandas.concat([ham, spam], ignore_index = True).to_csv(
        sys.stdout,
        header = True,
        encoding = 'utf-8',
        index = True,
        index_label = 'num'
    )

if __name__ == '__main__':
    main()
