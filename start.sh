#!/bin/bash

# Activate the conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate network

# Run the uvicorn command
uvicorn main:app --host 0.0.0.0 --port 1990 --reload
