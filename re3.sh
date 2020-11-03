#!/bin/bash

#SBATCH --job-name=moa_test
#SBATCH --cpus-per-task=10
#SBATCH --mem=64G
#SBATCH --ntasks=1
#SBATCH --time=23:59:00
#SBATCH --array=0-240
#SBATCH --partition=comp,short,gpu # himem, gquick

source myenv/bin/activate
time python2.7 ee3.py ${SLURM_ARRAY_TASK_ID} 1


exit 0
