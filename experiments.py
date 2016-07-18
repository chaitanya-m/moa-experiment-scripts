#! /usr/bin/python

##############################################################################################################
#
# Chaitanya Manapragada
#
# Generates multiple streams using MOA, waits until generation is completed, then averages data for all the streams
#
# Bug? Note that the "evaluation instances" field also gets averaged!!
# Also, the result has rows and columns swapped.
#
##############################################################################################################


import os, subprocess, shlex, shutil
import pandas as pd

MOA_DIR = '/home/chait/moa-release-2016.04/'

processes=[]

#Decision Stump... used for testing script.

moa_stump = "java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar"
moa_task = "moa.DoTask EvaluatePeriodicHeldOutTest"
task_options = "\"\"\" -l trees.DecisionStump -s generators.WaveformGenerator -n 10 -i 100 -f 20 \"\"\""
cmd_seq = (moa_stump, moa_task, task_options)

command = " ".join(cmd_seq)

decision_stump_dir = "decision_stump"

number_of_streams = 10

def main():
  os.chdir(MOA_DIR)
  remove_folder(decision_stump_dir)
  os.mkdir(decision_stump_dir)

  average_over_streams(number_of_streams, command, decision_stump_dir, "result")

  return 0



def average_over_streams(num_streams, command_line, output_folder, file_prefix):
  output_files = []
  folder_file_prefix = output_folder + "/" + file_prefix
  for stream_num in range(0, num_streams):
    output_files.append(folder_file_prefix + str(stream_num) + '.csv')
    run_experiment(command_line, output_files[stream_num])

  exit_codes = [p.wait() for p in processes]
  # wait until all experiments have finished running.

  print output_files

  dataframes = []
  for file_name in output_files:
    dataframes.append(pd.read_csv(file_name, index_col=False, header=0))
    # index_col has to be False as col 0 isn't integer

  all_stream_learning_data = pd.concat(dataframes)
  #all_stream_learning_data.to_csv("Cumulative.csv")

  all_stream_mean = {}
  for i in range(5): # 
    all_stream_mean[i] = all_stream_learning_data[i::number_of_streams].mean()
    #print all_stream_mean[i]
  all_stream_mean_df = pd.DataFrame(all_stream_mean)
  all_stream_mean_df.to_csv(folder_file_prefix + "Mean.csv")
    #print result_df
 

# Take a command line and create a process
def run_experiment(command_line, output_file):

  args = shlex.split(command_line)
  file_handle = output_file
  print(args)

  # create process
  with open(file_handle, "w+") as out:
    processes.append(subprocess.Popen(args, stdout=out))

  return

#Utilities
def remove_folder(path):
  if(os.path.exists)(path):
    shutil.rmtree(path)
  return

def make_folder(path):
  try:
    os.stat(path)
  except:
    os.mkdir(path)
  return

if __name__=="__main__":
  main()


# http://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
# https://docs.python.org/3.4/library/subprocess.html
# http://stackoverflow.com/questions/2331339/piping-output-of-subprocess-popen-to-files
# http://stackoverflow.com/questions/24765017/how-to-calculate-average-of-numbers-from-multiple-csv-files
# http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python

