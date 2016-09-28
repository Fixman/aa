#!/bin/bash

mkdir test
python make_dataframe.py --only $1 > test/data.csv
python extract_features.py -c dev/columns_a < test/data.csv > test/features_a.csv
python onehotencode.py -c dev/columns_b < test/data.csv > test/features_b.csv
python bagofwords.py dev/subject_words dev/body_words < test/data.csv > test/features_c.csv
python join_dataframes.py --columns_file dev/full_columns test/features_a.csv test/features_b.csv test/features_c.csv > test/features.csv
