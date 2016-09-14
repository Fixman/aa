#!/bin/bash
cat $1 | head -c 1000000 | sed 's/, "[^"]*$/]\n/' 
