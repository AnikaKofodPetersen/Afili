#!/bin/bash
./miniconda_check.py
conda config --add channels defaults > /dev/null 2>&1
conda config --add channels bioconda > /dev/null 2>&1
