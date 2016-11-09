#!/bin/bash
[ -e 'data' ] || mkdir data
pushd
cd data

wget https://dl.dropboxusercontent.com/u/6141633/dataset_dev.zip
unzip dataset_dev.zip
rm dataset_dev.zip
popd

make
