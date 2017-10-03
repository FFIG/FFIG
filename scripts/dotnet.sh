#!/usr/bin/env bash

set -e
set -u

src_dir=${1:-`pwd`}
gen_dir=${2:-`pwd`/build/generated}

cp ${src_dir}/tests/dotnet/*.cs ${gen_dir}
cp ${src_dir}/tests/dotnet/ffig.net.csproj ${gen_dir}

(cd ${gen_dir}; dotnet restore; LD_LIBRARY_PATH=${gen_dir} dotnet test)

