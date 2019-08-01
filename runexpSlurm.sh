#!/bin/bash

#SBATCH --job-name=moa_test
#SBATCH --cpus-per-task=5
#SBATCH --mem=32G
#SBATCH --ntasks=1
#SBATCH --time=4:00:00
#SBATCH --array=0-1039

source myenv/bin/activate
time python2.7 ensembleexp.py ${SLURM_ARRAY_TASK_ID} 1

exit 0
