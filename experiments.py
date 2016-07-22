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
import utilities

MOA_DIR = '/home/chait/moa-release-2016.04/'

processes=[]

#Decision Stump... used for testing script.

moa_stump = "java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar"
moa_task = "moa.DoTask EvaluatePeriodicHeldOutTest"
learner = "trees.DecisionStump"
generator = "generators.WaveformGenerator"

num_test_examples = 200 
num_instances = 3000 
test_interval = 100

num_rows = num_instances/test_interval


task_options = "\"\"\"" + " -l " + learner + " -s " + generator + " -n " + str(num_test_examples) + " -i " + str(num_instances) + " -f " + str(test_interval) + "\"\"\""

cmd_seq = (moa_stump, moa_task, task_options)

command = " ".join(cmd_seq)

decision_stump_dir = "decision_stump"

number_of_streams = 10

def main():

  #run_experiment("trees.DecisionStump", "generators.WaveformGenerator", 10, 100, 25, 10, "dec_stump", "res")
  experiment_average_over_streams(10, moa_stump + " " + "moa.DoTask EvaluateInterleavedTestThenTrain -l moa.classifiers.bayes.NaiveBayes -s \"\"\"(generators.categorical.AbruptDriftGenerator -b 1000)\"\"\" -i {i_val} -f {f_val} -q {q_val}".format(i_val = num_instances, f_val=test_interval, q_val=num_test_examples), "naive_bayes", "out")

  return 0

def run_experiment(learner, generator, num_test_examples, num_instances, test_interval, number_of_streams, output_dir, file_prefix):

  os.chdir(MOA_DIR)
  utilities.remove_folder(output_dir)
  utilities.make_folder(output_dir)

  num_rows = num_instances/test_interval

  task_options = "\"\"\"" + " -l " + learner + " -s " + generator + " -n " + str(num_test_examples) + " -i " + str(num_instances) + " -f " + str(test_interval) + "\"\"\""
  cmd_seq = (moa_stump, moa_task, task_options)
  command = " ".join(cmd_seq)

  
  experiment_average_over_streams(number_of_streams, command, output_dir, file_prefix)

  return

def experiment_average_over_streams(num_streams, command_line, output_folder, file_prefix):
  output_files = []

  os.chdir(MOA_DIR)
  utilities.remove_folder(output_folder)
  utilities.make_folder(output_folder)
  num_rows = num_instances/test_interval

  folder_file_prefix = output_folder + "/" + file_prefix
  #folder_file_prefix =  file_prefix
 
  for stream_num in range(0, num_streams):
    output_files.append(folder_file_prefix + str(stream_num) + '.csv')
  for stream_num in range(0, num_streams):
    print output_files[stream_num]
  for stream_num in range(0, num_streams):
    run_single_experiment(command_line, output_files[stream_num])

  exit_codes = [p.wait() for p in processes]
  # wait until all experiments have finished running.

  print output_files

  dataframes = []
  for file_name in output_files:
    print file_name
    dataframes.append(pd.read_csv(file_name, index_col=False, header=1, skiprows=0))
    #dataframes.append(pd.read_csv(file_name, index_col=False, header=0))
    # index_col has to be False as col 0 isn't integer

  all_stream_learning_data = pd.concat(dataframes)
  #all_stream_learning_data.to_csv("Cumulative.csv")

  all_stream_mean = {}
  for i in range(num_rows): # 
    all_stream_mean[i] = all_stream_learning_data[i::num_rows].mean()
    #print all_stream_mean[i]
  all_stream_mean_df = pd.DataFrame(all_stream_mean)
  all_stream_mean_df.to_csv(folder_file_prefix + "Mean.csv")
    #print result_df
 

# Take a command line and create a process
def run_single_experiment(command_line, output_file):

  args = shlex.split(command_line)
  #file_handle = os.path.join(MOA_DIR, output_file)
  file_handle = output_file
  print(args)
  print(file_handle) 

  
  # create process
  os.chdir(MOA_DIR)
  out1 = open(file_handle, "w+")

  processes.append(subprocess.Popen(args, stdout=out1))

if __name__=="__main__":
  main()


# http://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
# https://docs.python.org/3.4/library/subprocess.html
# http://stackoverflow.com/questions/2331339/piping-output-of-subprocess-popen-to-files
# http://stackoverflow.com/questions/24765017/how-to-calculate-average-of-numbers-from-multiple-csv-files
# http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python

