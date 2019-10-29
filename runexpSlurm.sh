#!/bin/bash

#SBATCH --job-name=moa_test
#SBATCH --cpus-per-task=10
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --time=00:59:00
#SBATCH --array=0-127
#SBATCH --partition=comp,gpu,gquick,short,himem

source myenv/bin/activate
time python2.7 ensembleexp.py ${SLURM_ARRAY_TASK_ID} 1

exit 0
