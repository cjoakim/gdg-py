#!/bin/bash

mkdir -p tmp/epoch
mkdir -p tmp/generations
mkdir -p tmp/ts_utc 
mkdir -p tmp/ts_utc

echo 'executing unit tests with code coverage ...'
python -m pytest --cov=gdg/ --cov-report html tests/
