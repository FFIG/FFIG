#!/usr/bin/env bash

set -e
set -u

gen_dir=${1:-`pwd`/build/generated}

(cd ${gen_dir}; dotnet restore; LD_LIBRARY_PATH=${gen_dir} dotnet test -o .)

