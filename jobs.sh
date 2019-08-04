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
