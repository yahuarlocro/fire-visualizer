#!/bin/bash
#title           :build_testing.sh
#description     :This script fulfills 2 functions:
#                :1. build docker image locally and sets a new tag for "testing"
#                :image
#                :2. create docker image locally
#author          :yahuarlocro
#date            :2023-06-09
#version         :0.1
#usage           :bash build.sh
#                :./build.sh
#dependecies     : 
#==============================================================================

# exit on error
set -e

# function to remove all directories and files when wheel file was 
# created
# function cleanup_and_exit
function cleanup
{
    # remove all wheel-files from dockersetup directory
    rm -rf {./dockersetup/config.py,./dockersetup/main.py,./dockersetup/dist,./dist}

    # exit 0
}

# clean up local directory for possible existent dist and code files
cleanup

# exits if python3 is not installed or default version 
if ! hash python3.11; then
    echo -e "\n##############################################################"
    echo "python3.11 is not installed"
    echo -e "##############################################################\n"
    exit 1
fi

# install with poetry
poetry install
# create wheel file

poetry build

IMAGE_TAG=$(poetry version --short)

WHL_FILE=$(find ./dist -maxdepth 1 -type f -iname "*.whl")

if [[ -n "${WHL_FILE}" ]]
then
    # WHL_FILENAME=$(basename ${WHL_FILE})
    
    rsync -a ./dist dockersetup/
    rsync -a ./src/main.py ./src/config.py dockersetup/
    cd ./dockersetup

    # build docker image
    docker build --no-cache -t visualizer:${IMAGE_TAG} --build-arg WHL_FILENAME=${WHL_FILE} .
    echo -e "\n##############################################################"
    echo "docker image(testing) was built successfully"
    echo -e "##############################################################\n"

    cd ..
else
    echo -e "\n##############################################################"
    echo "no wheel file found"
    echo -e "##############################################################\n"
fi


# clean up local directory
# cleanup_and_exit
cleanup