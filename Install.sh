#!/bin/bash
./miniconda_check.py
conda config --add channels defaults > /dev/null 2>&1
conda config --add channels bioconda > /dev/null 2>&1

eval "$(conda shell.bash hook)"
conda env create -f afili_env.yml 2> /dev/null
conda activate afili_env
prokka --setupdb 
parallel --citation
conda deactivate


