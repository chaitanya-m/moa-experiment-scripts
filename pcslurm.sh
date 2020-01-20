#!/bin/bash

#SBATCH --job-name=moa_test
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --ntasks=1
#SBATCH --time=3-00:00:00
#SBATCH --partition=short,comp
#SBATCH --array=1-2

source myenv/bin/activate
time python2.7 ensembleexp.py ${SLURM_ARRAY_TASK_ID} 21

exit 0
