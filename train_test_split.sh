#!/bin/bash
set -e

split=$(mktemp)
cat $1 | sed -E 's/([^\\]",|\^[|\]$)\s*/\1\n/g' > $split

lines=$(wc -l $split | cut -f1 -d' ')
test_lines=$((lines / 10))

( head -n -$test_lines $split | sed '$s/,//' ; echo ']' ) > $(sed -E 's/_\w+\./_train./' <<< $1)
( echo '['; tail -n $test_lines $split ) > $(sed -E 's/_\w+\./_test./' <<< $1)
