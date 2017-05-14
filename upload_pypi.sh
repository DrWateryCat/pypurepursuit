#!/bin/sh

rm -rf dist
python3.5 setup.py bdist_wheel
twine upload dist/*
