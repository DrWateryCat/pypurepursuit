#!/bin/sh

python3.5 setup.py bdist_wheel
cd dist
sudo -H pip3.5 uninstall pypurepursuit
sudo -H pip3.5 install pypurepursuit*.whl
