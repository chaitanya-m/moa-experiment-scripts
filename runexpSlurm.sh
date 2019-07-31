#!/bin/bash

#SBATCH --nodes=2
#SBATCH --job-name=moa_test
#SBATCH --cpus-per-task=12
#SBATCH --ntasks-per-node=4
#SBATCH --mincpus=12
#SBATCH --mem-per-cpu=5G

#for i in `seq 100`; do  
#srun --exclusive --nodes 1 --ntasks 1 ./program ${i} &
#done
#wait


source myenv/bin/activate

for i in {0..51}
do
srun --nodes=1 time python2.7 ensembleexp.py $i 10 &
done
wait
