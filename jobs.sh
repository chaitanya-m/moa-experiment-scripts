
sbatch --mem=10G --array [418-498:20] runexpSlurm.sh
#sbatch --mem=10G --array [19-1039:20] runexpSlurm.sh

sbatch --mem=48G --array [240-1039:20] --time 4-00:00:00 --cpus-per-task 10 runexpSlurm.sh

sbatch --mem=18G --array [81-1039:20] runexpSlurm.sh

sbatch --mem=18G --array [342-542:20] runexpSlurm.sh
sbatch --mem=18G --array [223-1039:20] --time 4-00:00:00 --cpus-per-task 10 runexpSlurm.sh
sbatch --mem=18G --array [24-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [45-1039:20] runexpSlurm.sh 

sbatch --mem=18G --array [46-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [127-1039:20] runexpSlurm.sh #7.5G 27 min
sbatch --mem=18G --array [8-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [9-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [10-1039:20] runexpSlurm.sh

sbatch --mem=18G --array [131-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [92-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [13-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [14-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [15-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [16-1039:20] runexpSlurm.sh
sbatch --mem=18G --array [17-1039:20] runexpSlurm.sh

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
