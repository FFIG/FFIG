#!/bin/sh

# Travis CI `install` phase for Linux.
# Build a docker image. The base image contains all of the dependencies.

docker pull ffig/ffig-base
docker build -t ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} .
