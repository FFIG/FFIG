#!/bin/sh

find ffig scripts tests -name \*.py -exec autopep8 --in-place --aggressive --aggressive {} +
