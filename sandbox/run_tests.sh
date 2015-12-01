#!/usr/bin/env bash
clang++ -std=c++14 -shared -Wl, -o libTree_c.dylib -fPIC Tree.cpp || return -1

python -m nose test.py


