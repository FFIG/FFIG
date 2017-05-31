#!/bin/sh

# Travis CI `script` phase for Linux.
# Run ffig build inside Docker

docker run ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} /bin/bash -c "./scripts/build.py -T \"CPP|MOCKS\" -c ASAN"
docker run ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} /bin/bash -c "./scripts/build.py -T \"CPP|MOCKS\" -c ASAN --python-path python3"
docker run ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} /bin/bash -c "./scripts/build.py -t"
docker run ${DOCKER_REPOSITORY}:${TRAVIS_COMMIT} /bin/bash -c "./scripts/build.py -t --python-path python3"
