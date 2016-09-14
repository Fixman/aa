#!/bin/bash
	set -e
set -x

split=$(mktemp)
cat $1 | sed -E 's/([^\\]"(,|\])|^\[)\s*/\1\
/g'> $split

lines=$(wc -l $split | sed -E 's/^.* ([0-9]+) .*/\1/')
other_lines=$((lines - lines / 10))
	test_lines=$((lines / 10))

( head -n $other_lines $split | sed '$s/,\s*$//' ; echo ']' ) > $(sed -E 's/_dev+\./_train./' <<< $1)
( echo '['; tail -n $test_lines $split ) > $(sed -E 's/_dev+\./_test./' <<< $1)

rm -f $split
