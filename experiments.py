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

num_test_examples = 200 
num_instances = 3000 
test_interval = 100

moa_stump = "java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar"
moa_task = "moa.DoTask EvaluateInterleavedTestThenTrain"
learner = "-l moa.classifiers,bayes.NaiveBayes"
generator = "-s \"\"\"(generators.categorical.AbruptDriftGenerator -b 1000)\"\"\""


num_rows = num_instances/test_interval

cmd_seq = [moa_stump, moa_task, learner, generator, "-i {i_val} -f {f_val} -q {q_val}".format(i_val = num_instances, f_val=test_interval, q_val=num_test_examples)]
cmd = " ".join(cmd_seq) 

number_of_streams = 10

def main():

  cmd = moa_stump + " " + "moa.DoTask EvaluateInterleavedTestThenTrain -l moa.classifiers.bayes.NaiveBayes -s \"\"\"(generators.categorical.AbruptDriftGenerator -b 1000)\"\"\" -i {i_val} -f {f_val} -q {q_val}".format(i_val = num_instances, f_val=test_interval, q_val=num_test_examples)
  mse = MultiStreamExperiment()
  mse.average_over_streams(number_of_streams , cmd, "naive_bayes", "out")

  return 0

# Composite of many instances of a given experiment running in parallel. Note that the seed for the random generator must change!
class MultiStreamExperiment:

  # Multiple stream Processes for this experiment
  # https://docs.python.org/3/tutorial/classes.html
  # Note that this is the way to create instance-specific variables- in init.
  # Anything outside would be shared across all instances.

  def __init__(self):
    self.processes = []  

  # The MOA processes created by the Experiment.run() method write to output files. Average over these.
  def average_over_streams(self, num_streams, command_line, output_folder, file_prefix):
    output_files = []
  
    os.chdir(MOA_DIR)
    utilities.remove_folder(output_folder)
    utilities.make_folder(output_folder)
    num_rows = num_instances/test_interval
  
    folder_file_prefix = output_folder + "/" + file_prefix
    # folder_file_prefix =  file_prefix
   
    # Create file names
    for stream_num in range(0, num_streams):
      output_files.append(folder_file_prefix + str(stream_num) + '.csv')
    # Print them
    for stream_num in range(0, num_streams):
      print output_files[stream_num]
    # Run experiments setting output files
    for stream_num in range(0, num_streams):
      e = Experiment()
      e.run(command_line ,output_files[stream_num], self.processes)
  
    exit_codes = [p.wait() for p in self.processes]
    # wait until all experiments have finished running: each experiment corresponds to a process.
  
    print output_files
  
    # Load the outputs into dataframes to prepare for averaging
  
    dataframes = []
    for file_name in output_files:
      print file_name
      dataframes.append(pd.read_csv(file_name, index_col=False, header=1, skiprows=0))
      # index_col has to be False as col 0 isn't integer
  
    # Concatenate all of these. This creates a very large file
    # In order to make this faster, maybe just add values from other files into one file
    all_stream_learning_data = pd.concat(dataframes)
    all_stream_learning_data.to_csv(folder_file_prefix+"Cumulative.csv")
  
    all_stream_mean = {}
    # average row by row
    for i in range(num_rows): 
      all_stream_mean[i] = all_stream_learning_data[i::num_rows].mean()
      #print all_stream_mean[i]
    all_stream_mean_df = pd.DataFrame(all_stream_mean)
    all_stream_mean_df.to_csv(folder_file_prefix + "Mean.csv")
    # Print result to file 

#class SeededExperiment(Experiment):

#  def __init__(self, seed):
#    self.seed = seed

class Experiment:
  
  # Take a command line and create a MOA process, which outputs results to a file.
  def run(self, cmd, output_file, processes):
  
    args = shlex.split(cmd)
    file_handle = output_file

    #file_handle = os.path.join(MOA_DIR, output_file)
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

