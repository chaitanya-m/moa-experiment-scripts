#!/bin/bash

#SBATCH -N 10
#SBATCH --job-name=moa_test
#SBATCH --cpus-per-task=12
#SBATCH --mem=355G
#SBATCH --ntasks-per-node=10
#SBATCH --mincpus=12
#SBATCH --mem-per-cpu=3G

#for i in `seq 100`; do  
#srun --exclusive --nodes 1 --ntasks 1 ./program ${i} &
#done
#wait


srun --ntasks=1 echo "hello" & 
srun --ntasks=1 sleep 1 &
srun --ntasks=1 echo "Running Experiments" &

for i in {0..1}
do
srun --ntasks=1 time python2.7 ensembleexp.py $i
wait
done
source myenv/bin/activate
