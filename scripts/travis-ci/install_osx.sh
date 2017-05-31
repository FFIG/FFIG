#!/bin/sh

# Travis CI `install` phase for macOS.
# Install ffig dependencies.

# Homebrew packages
brew install cmake
brew install go
brew install ninja

# Python 2 packages
pip2 install --upgrade pip
pip2 install jinja2 nose backports.typing

# Python 3 packages
pip3 install --upgrade pip
pip3 install jinja2 nose

# Ruby packages
gem install ffi

