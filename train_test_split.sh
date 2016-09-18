#!/bin/bash
set -e
set -x

split=$(mktemp)
cat $1 | sed -E 's/([^\\]",|^\[|\]$)\s*/\1\n/g' > $split

lines=$(wc -l $split | sed -E 's/^\s*([0-9]+).*/\1/')
test_lines=$((lines / 10))

( head -n -$test_lines $split | sed '$s/,\s*$//' ; echo ']' ) > $(sed -E 's/_\w+\./_train./' <<< $1)
( echo '['; tail -n $test_lines $split ) > $(sed -E 's/_\w+\./_test./' <<< $1)

# rm -f $split
