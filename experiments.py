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
# By default a different random seed seems to be picked by the Categorical Abrupt Drift Generator for each stream.
##############################################################################################################

import os, subprocess, shlex, shutil
import moa_command_vars as mcv
import pandas as pd
import utilities
import matplotlib.pyplot as plt
import matplotlib

processes=[]

num_instances = 3000 
test_interval = 100
num_test_examples = 200

num_rows = num_instances/test_interval

number_of_streams = 10

def main():

  cmd = " ".join([mcv.MOA_STUMP, mcv.MOA_TASK_EITTT, mcv.MOA_LEARNER_NAIVE_BAYES, mcv.GeneratorBuilder.CategoricalAbruptDriftGenBuilder(None, None, 1000, None, None, None, False, False, None).cmd(), mcv.setTrainingTestingParams(num_instances, test_interval, num_test_examples)])
  mse = MultiStreamExperiment()
  mse.average_over_streams(number_of_streams , cmd, mcv.OUTPUT_DIR, mcv.OUTPUT_PREFIX)

  return 0

class Plot:
  # Assumption: Received data contains a correctly computed error column 

  #def __init__(self):

  @staticmethod
  def plot_df(data_frame):
    matplotlib.style.use('ggplot')
    data_frame.plot(x='learning evaluation instances', y='error')
    plt.show()


# This is a composite of a Generator, Learner, and Evaluator
#class CompositeExperiment(MultiStreamExperiment):

# This is an experiment with a single set of  
#class SingleExperiment(MultiStreamExperiment):



# Composite of many instances of a given experiment running in parallel. 
# Note that the seed for the random generator must change!
# Multiple stream Processes for an experiment
class MultiStreamExperiment:

  def __init__(self):
    self.processes = []  
  # Note that this is the way to create instance-specific variables- in init.
  # Anything outside would be shared across all instances.

  # Create individual MOA processes, write to CSV output files. Average over these.
  def average_over_streams(self, num_streams, command_line, output_folder, file_prefix):
    output_files = []
  
    os.chdir(mcv.MOA_DIR)
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
      e = Stream()
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
    all_stream_learning_data.to_csv(folder_file_prefix + "Cumulative.csv")

    all_stream_mean = {}
    # average row by row
    for i in range(num_rows): 
      all_stream_mean[i] = all_stream_learning_data[i::num_rows].mean()

    #all_stream_mean_df = pd.DataFrame(all_stream_mean)
    all_stream_mean_df = pd.DataFrame(all_stream_mean).transpose() 

    all_stream_mean_df.to_csv(folder_file_prefix + "Mean.csv")
    # Print result to file 
    
    all_stream_mean_df['error'] = (100.0 - all_stream_mean_df['classifications correct (percent)'])/100.0

    Plot.plot_df(all_stream_mean_df)

# A single MOA command creating a single MOA process
class Stream:
  
  # Take a command line and create a MOA process, which outputs results to a file.
  def run(self, cmd, output_file, processes):
  
    args = shlex.split(cmd)

    print(args)
    print(output_file) 
    
    # create process
    output_file = open(output_file, "w+")
  
    processes.append(subprocess.Popen(args, stdout=output_file))

if __name__=="__main__":

  main()


# http://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
# https://docs.python.org/3.4/library/subprocess.html
# http://stackoverflow.com/questions/2331339/piping-output-of-subprocess-popen-to-files
# http://stackoverflow.com/questions/24765017/how-to-calculate-average-of-numbers-from-multiple-csv-files
# http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
# http://stackoverflow.com/questions/4555932/public-or-private-attribute-in-python-what-is-the-best-way

