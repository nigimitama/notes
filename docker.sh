#!/bin/bash

function build() {
    docker build . -t node
}

function up() {
    docker run \
        -it \
        --mount type=bind,source="$(pwd)",target=/root \
        node
}

if [ ${1} == "build" ]; then
    build
elif [ ${1} == "up" ]; then
    up
else
    echo "unexpected command."
fi
