#!/bin/bash

mkdir -p tmp/epoch
mkdir -p tmp/generations
mkdir -p tmp/ts_utc 
mkdir -p tmp/ts_utc

echo 'executing unit tests with code coverage ...'
python -m pytest --cov=gdg/ --cov-report html tests/



# For sdist deployment to PyPi, or local PyPi server:
# python setup.py sdist
# python setup.py sdist upload
# python setup.py sdist upload -r local
# python setup.py sdist upload -r pypilegacy
# ls -al /Users/cjoakim/pypi-packages
# rm /Users/cjoakim/pypi-packages/gdg*
