#!/bin/bash

#SBATCH --job-name=moa_test
#SBATCH --cpus-per-task=5
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --time=00:59:00
#SBATCH --array=0-31
#SBATCH --partition=comp,short,himem,gpu # gquick

source myenv/bin/activate
time python2.7 ensembleexp.py ${SLURM_ARRAY_TASK_ID} 1

exit 0
