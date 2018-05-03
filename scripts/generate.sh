#!/usr/bin/env bash

mkdir -p build

(cd build; cmake -G Ninja ..)

# Minimal target to generate Boost-python bindings.
(cd build && ninja Shape_c)

set -x
clang++ -std=c++14 build/generated/Shape.py.cpp -c -Iffig/include/ $(python3-config --includes)
