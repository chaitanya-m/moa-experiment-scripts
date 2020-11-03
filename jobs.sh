# redo failed tasks
#sbatch --mem=24G --array [343-1039:20] --time 4-00:00:00 --cpus-per-task 10 runexpSlurm.sh
#sbatch --mem=30G --array [342,402,522,542,163,321,381,342,522,542,184,304,324,344,404,444,524,544,547,188,408,548,329,412] --cpus-per-task 10 runexpSlurm.sh


# These indices can be readjusted... they have been in fact to account for changed RAM requirements for some tasks
# Reset to 0 - num(datasets) when done (20 datasets initially)
#sbatch --mem=10G --array [418-498:20] runexpSlurm.sh
#sbatch --mem=10G --array [19-1039:20] runexpSlurm.sh
#
#sbatch --mem=48G --array [240-1039:20] --time 4-00:00:00 --cpus-per-task 10 runexpSlurm.sh
#
#sbatch --mem=18G --array [81-1039:20] runexpSlurm.sh
#
#sbatch --mem=24G --array [342-542:20] runexpSlurm.sh
#sbatch --mem=24G --array [223-1039:20] --time 4-00:00:00 --cpus-per-task 10 runexpSlurm.sh
#sbatch --mem=24G --array [24-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [45-1039:20] runexpSlurm.sh 
#
#sbatch --mem=18G --array [46-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [127-1039:20] runexpSlurm.sh #7.5G 27 min but goes up to 18G
#sbatch --mem=18G --array [8-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [9-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [10-1039:20] runexpSlurm.sh
#
#sbatch --mem=18G --array [131-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [92-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [13-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [14-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [15-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [16-1039:20] runexpSlurm.sh
#sbatch --mem=18G --array [17-1039:20] runexpSlurm.sh
#


#Unshuffled
#sbatch --mem-per-cpu=5G --array [0-1039] --time 3:00:00 --cpus-per-task 1 --partition=short,comp,gpu runexpSlurm.sh

# Synthetic (with proper indices!)
#sbatch --mem=20G --array [0-1247] --time 5:00:00 --cpus-per-task 10 --partition=short,comp,gpu runexpSlurm.sh


#             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
#4682512_[8-1028:20      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682513_[9-1029:20      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682514_[10-1030:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682517_[13-1033:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682518_[14-1034:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682519_[15-1035:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682520_[16-1036:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682521_[17-1037:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682509_[45-1025:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682515_[131-1031:      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682516_[92-1032:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682508_[24-1024:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682505_[81-1021:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682510_[46-1026:2      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682511_[127-1027:      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682504_[240-1020:      comp moa_test   cman39 PD       0:00      1 (Priority)
#4682507_[223-1023:      comp moa_test   cman39 PD       0:00      1 (Priority)
#       4682507_163      comp moa_test   cman39  R    2:04:23      1 mi15
#       4682507_183      comp moa_test   cman39  R    1:17:01      1 mi08
#       4682507_203      comp moa_test   cman39  R       9:42      1 mi08
#       4682504_220      comp moa_test   cman39  R      20:16      1 hc09
#       4682504_200      comp moa_test   cman39  R      23:01      1 hc09
#       4682504_180      comp moa_test   cman39  R    1:03:42      1 mi08

#Failed tasks memory (grep: memory)

#slurm-4682506_342.out
#slurm-4682506_402.out
#slurm-4682506_522.out
#slurm-4682506_542.out
#slurm-4682507_163.out
#slurm-4682978_321.out
#slurm-4682978_381.out
#slurm-4682979_342.out
#slurm-4682979_522.out
#slurm-4682979_542.out
#slurm-4682981_184.out
#slurm-4682981_304.out
#slurm-4682981_324.out
#slurm-4682981_344.out
#slurm-4682981_404.out
#slurm-4682981_444.out
#slurm-4682981_524.out
#slurm-4682981_544.out
#slurm-4682984_547.out
#slurm-4682985_188.out
#slurm-4682985_408.out
#slurm-4682985_548.out
#slurm-4682986_329.out
#slurm-4682989_412.out



#slurm-4682980_343.out
#slurm-4682980_403.out
#slurm-4682980_423.out
#slurm-4682980_443.out

#Failed tasks time (grep: cancel)

#slurm-4684694_163.out

# Task Failed MOA Error (grep: task failed)

#slurm-4682990_653.out
#slurm-4682990_693.out
#slurm-4682990_773.out
#slurm-4682990_793.out

# Processing results
#(myenv) [cman39@monarch-login1 moa-experiment-scripts]$ srun --mem=20G --time 5:00:00 --cpus-per-task 2 --partition=short,comp,gpu python ensembleexp.py
#srun: job 4693727 queued and waiting for resources
#srun: job 4693727 has been allocated resources
#:q
#
#Process Process-1:
#Traceback (most recent call last):
#  File "/usr/lib64/python2.7/multiprocessing/process.py", line 258, in _bootstrap
#    self.run()
#  File "/usr/lib64/python2.7/multiprocessing/process.py", line 114, in run
#    self._target(*self._args, **self._kwargs)
#  File "ensembleexp.py", line 975, in chart24
#    makeChart("Diversity vs Adaptation", learners, generators, evaluators, str('24'))
#  File "ensembleexp.py", line 189, in makeChart
#    dataframes.append(pd.read_csv(this_file, index_col=False, header=0, skiprows=0))
#  File "/home/cman39/moa-experiment-scripts/myenv/lib/python2.7/site-packages/pandas/io/parsers.py", line 702, in parser_f
#    return _read(filepath_or_buffer, kwds)
#  File "/home/cman39/moa-experiment-scripts/myenv/lib/python2.7/site-packages/pandas/io/parsers.py", line 435, in _read
#    data = parser.read(nrows)
#  File "/home/cman39/moa-experiment-scripts/myenv/lib/python2.7/site-packages/pandas/io/parsers.py", line 1139, in read
#    ret = self._engine.read(nrows)
#  File "/home/cman39/moa-experiment-scripts/myenv/lib/python2.7/site-packages/pandas/io/parsers.py", line 1995, in read
#    data = self._reader.read(nrows)
#  File "pandas/_libs/parsers.pyx", line 899, in pandas._libs.parsers.TextReader.read
#  File "pandas/_libs/parsers.pyx", line 914, in pandas._libs.parsers.TextReader._read_low_memory
#  File "pandas/_libs/parsers.pyx", line 968, in pandas._libs.parsers.TextReader._read_rows
#  File "pandas/_libs/parsers.pyx", line 955, in pandas._libs.parsers.TextReader._tokenize_rows
#  File "pandas/_libs/parsers.pyx", line 2172, in pandas._libs.parsers.raise_parser_error
#ParserError: Error tokenizing data. C error: Expected 1 fields in line 9, saw 18

# Something is wrong with line 9 of a file

# find . -type f -wholename "*shuf*" | xargs --replace sed '9q;d' {} > ~/temp0
# awk 'NF > 2 { print NR }' temp0 | xargs --replace sed '{}q;d' temp0

# the errant line 9s look like this:
#learning evaluation instances,evaluation time (cpu seconds),model cost (RAM-Hours),classified instances,classifications correct (percent),Kappa Statistic (percent),Kappa Temporal Statistic (percent),Kappa M Statistic (percent),model training instances,model serialized size (bytes),tree size (nodes),tree size (leaves),active learning leaves,tree depth,active leaf byte size estimate,inactive leaf byte size estimate,byte size estimate overhead,splits

# There are 16 of them
 
#7621
#7622
#7624
#7625
#7626
#7628
#7629
#7630
#10261
#10262
#10264
#10265
#10266
#10268
#10269
#10270
#

# Listing the files and looking at them... there's debug output in the header hence the issues.
#xxxxxxxxxxxxxx
#false
#false
#false
#xxxxxxxxxxxxxx
#false
#false
#false
#


######################################################################################3
#sbatch --mem=32G --array=[20-23,52-55,58,73-79,80-83] runexpSlurm.sh 
#For Levbag, around 8 synthetic streams, and for SRP 8 synthetic streams need 32GB
#for srp synthetic, around 8 streams needed more than 32gb 84-87, 118-119. 

######################################################################################


######
#this is with 64 GB memory for HAT(original, with unspecified features) ensembles...
#OzaBoostAdwin with tnebshuf, covpokelecshuf 
#####
#slurm-6493217_106.out:java.io.IOException: Cannot allocate memory
#slurm-6493217_106.out:slurmstepd: error: Detected 9 oom-kill event(s) in step 6493531.batch cgroup. Some of your processes may have been killed by the cgroup out-of-memory handler.

#slurm-6493217_115.out:Task failed. Reason: stackoverflowerror
#increased stack size to 24g from 12g!


#####
#slurm-6493217_140.out:java.io.IOException - memory
#BOLE with font shuf 

#slurm-6493217_144.out:java.io.IOException: Cannot allocate memory
#BOLE with aws shuf 
####

####
#slurm-6493217_160.out:slurmstepd: error: Detected 15 oom-kill event(s) in step 6493906.batch cgroup. Some of your processes may have been killed by the cgroup out-of-memory handler.
#OnlineSmoothBoost with Fonts
####

