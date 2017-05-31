#!/bin/sh

# Travis CI `script` phase for macOS.
# Run ffig build.

./scripts/build.py -t
./scripts/build.py -t --python-path python3
