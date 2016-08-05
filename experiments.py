
import os, subprocess, shlex, shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

import utilities
import generators as gen
import learners as lrn
import evaluators as evl
import moa_command_vars as mcv

class Plot:
  # Assumption: Received data contains a correctly computed error column 

  #def __init__(self):

  @staticmethod
  def plot_df(data_frame):
    matplotlib.style.use('ggplot')
    #plt.figure() 
    #data_frame.plot(x='learning evaluation instances')
    data_frame.plot()
    plt.show()

# Composite of many instances of a given experiment running in parallel. 
# Note that the seed for the random generator must change!
# Multiple stream Processes for an experiment
class ExperimentRunner:

  processes = [] 

  @classmethod
  def runExperiments(this):
    output_files = []

    os.chdir(mcv.MOA_DIR)
    utilities.remove_folder(mcv.OUTPUT_DIR)
    utilities.make_folder(mcv.OUTPUT_DIR)
    

    prior_drift_mag_exp = CompositeExperimentBuilder.varyPriorDriftMagBuilder(mcv.NUM_STREAMS, mcv.OUTPUT_DIR, mcv.OUTPUT_PREFIX, this.processes)

    for exp in prior_drift_mag_exp.getExperiments():
      exp.run(this.processes)
      # Run experiments setting output files

    exit_codes = [p.wait() for p in this.processes]
    # wait until all experiments have finished running: each experiment corresponds to a process.

    output_files = prior_drift_mag_exp.getOutputFiles()

    # List of mean_dataframes
    mean_dataframes = []
    # Dataframe that contains all the mean error columns for the experiments
    error_df = pd.DataFrame([])

    # Load the outputs into dataframes to prepare for averaging
    # output_files is a 2D list. It has a folder-file structure.
    for folder, files in output_files.iteritems():
      # List of dataframes in this folder
      dataframes = []
      for this_file in files:
        dataframes.append(pd.read_csv(this_file, index_col=False, header=0, skiprows=prior_drift_mag_exp.getSkipRows()))
        # index_col has to be False as col 0 isn't integer

      # Concatenate all of these. This creates a very large file
      # In order to be memory efficient, maybe just add values from other files into one file
      all_stream_learning_data = pd.concat(dataframes)
      #all_stream_learning_data.to_csv(folder_file_prefix + "Cumulative.csv")
  
      all_stream_mean = {}
      # average row by row
      for i in range(mcv.NUM_ROWS): 
        all_stream_mean[i] = all_stream_learning_data[i::mcv.NUM_ROWS].mean()
  
      all_stream_mean_df = pd.DataFrame(all_stream_mean).transpose() 
      #all_stream_mean_df.to_csv(folder_file_prefix + "Mean.csv")
      
      all_stream_mean_df['error'] = (100.0 - all_stream_mean_df['classifications correct (percent)'])/100.0

      # Add this folder's mean error column to the error_df 
      error_df[str(folder)] = all_stream_mean_df['error'] 
      mean_dataframes.append(all_stream_mean_df)

    # Set the index column
    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    error_df = error_df.set_index(mcv.INDEX_COL)
    error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

      #Plot.plot_df(all_stream_mean_df)
    Plot.plot_df(error_df)
   

# A single MOA command creating a single MOA process
class Experiment:
 
  def __init__(self, stump, e, l, g, params, output_file, processes):
    self.cmd = " ".join([stump, e.cmd(), l.cmd(), g.cmd(), params]) 
    self.output_file = output_file
    self.processes = processes 
  # Take a command line and create a MOA process, which outputs results to a file.
  def run(self, processes):
  
    args = shlex.split(self.cmd)

    print(args)
    print(self.output_file) 
    
    # create process
    output_file = open(self.output_file, "w+")
  
    processes.append(subprocess.Popen(args, stdout=output_file))

class ExperimentBuilder:

  @staticmethod
  def PriorDriftMagBuilder(driftMag, output_file, processes):
    evaluator = evl.EvaluatorBuilder.EvaluatePrequentialBuilder()
    learner = lrn.LearnerBuilder.NaiveBayesLearnerBuilder()
    generator = gen.GeneratorBuilder.CategoricalAbruptDriftGenBuilder(nAttributes=2, nValuesPerAttribute=2, burnIn=1000, driftMagPrior=driftMag, driftPrior=True)

    e = Experiment(mcv.MOA_STUMP, evaluator, learner, generator, mcv.PARAMS, output_file, processes)
    return e 
  @staticmethod
  def ConditionalDriftMagBuilder(driftMag, output_file, processes):
    evaluator = evl.EvaluatorBuilder.EvaluateInterleavedTestThenTrainBuilder()
    learner = lrn.LearnerBuilder.NaiveBayesLearnerBuilder()
    generator = gen.GeneratorBuilder.CategoricalAbruptDriftGenBuilder(burnIn=1000, driftMagConditional=driftMag, driftConditional=True)

    e = Experiment(mcv.MOA_STUMP, evaluator, learner, generator, mcv.PARAMS, output_file, processes)
    return e 

class CompositeExperiment:

  def __init__(self, exp_list, output_files, skip_rows):
    self.exp_list = exp_list
    self.output_files = output_files
    self.skip_rows = skip_rows
  def getExperiments(self):
    return self.exp_list
  def getOutputFiles(self):
    return self.output_files
  def getSkipRows(self):
    return self.skip_rows


class CompositeExperimentBuilder:

  @staticmethod
  def varyPriorDriftMagBuilder(num_streams, output_folder, file_prefix, processes):
    skip_rows = 3
    exp_list = []
    output_files = {} # dictionary mapping each experiment folder to the files contained within
    drift_mag_list = [1.0e-20, 0.3, 0.7, 0.9]

    # Create a separate folder for each drift magnitude.
    for drift_mag in drift_mag_list:
      this_output_folder = output_folder + '/' + str(drift_mag)
      folder_file_prefix = this_output_folder + '/' + file_prefix
      utilities.remove_folder(this_output_folder)
      utilities.make_folder(this_output_folder)
      this_folder_output_files = []

      for i in range(0, num_streams):
        output_file = folder_file_prefix + str(i) + '.csv'
        this_folder_output_files.append(output_file)
        exp_list.append(ExperimentBuilder.PriorDriftMagBuilder(drift_mag, output_file, processes))

      output_files[drift_mag] = this_folder_output_files

    return CompositeExperiment(exp_list, output_files, skip_rows)


  @staticmethod
  def varyConditionalDriftMagBuilder(num_streams, output_folder, file_prefix, processes):
    skip_rows = 2
    exp_list = []
    output_files = {} # dictionary mapping each experiment folder to the files contained within
    drift_mag_list = [1.0e-20, 0.25, 0.5, 0.7]

    # Create a separate folder for each drift magnitude.
    for drift_mag in drift_mag_list:
      this_output_folder = output_folder + '/' + str(drift_mag)
      folder_file_prefix = this_output_folder + '/' + file_prefix
      utilities.remove_folder(this_output_folder)
      utilities.make_folder(this_output_folder)
      this_folder_output_files = []

      for i in range(0, num_streams):
        output_file = folder_file_prefix + str(i) + '.csv'
        this_folder_output_files.append(output_file)
        exp_list.append(ExperimentBuilder.ConditionalDriftMagBuilder(drift_mag, output_file, processes))

      output_files[drift_mag] = this_folder_output_files

    return CompositeExperiment(exp_list, output_files, skip_rows)

