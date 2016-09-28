#!/bin/bash

mkdir test
python make_dataframe.py --only $1
python extract_features.py -c dev/columns_a < $1 > test/features_a.csv
python onehotencode.py -c dev/columns_b < $1 > test/features_b.csv
python bagofwords.py dev/subject_words dev/body_words > test/features_c.csv
python join_dataframes --columns_file dev/full_columns > test/features.csv
