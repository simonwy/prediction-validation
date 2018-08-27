#!/bin/bash
#
# This is the shell script to compile my Python code and then execute it.

python ./src/prediction-validation.py ./input/window.txt ./input/actual.txt ./input/predicted.txt ./output/comparison.txt
