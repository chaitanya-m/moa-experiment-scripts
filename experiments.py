
import os, subprocess, shlex, shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import pylab
import numpy as np

import re
import utilities
import math
import generators as gen
import learners as lrn
import evaluators as evl
import moa_command_vars as mcv
from textwrap import wrap
from collections import OrderedDict

import listOfLearners

class Plot:
  # Assumption: Received data contains a correctly computed error column 

  #def __init__(self):

  @staticmethod
  def plot_df(data_frame, cmd, figPath, df_aux = None):

   # matplotlib.rcParams.update({'font.size': 24})
    # theres a whole bunch of available styles
    matplotlib.style.use('seaborn-paper')
#   styles = ['seaborn-darkgrid', 'seaborn-white', 'fivethirtyeight', 'seaborn-bright', 'seaborn-pastel', 'ggplot', 'classic', 'seaborn-notebook', '_classic_test', 'seaborn-ticks', 'seaborn-poster', 'dark_background', 'seaborn-paper', 'seaborn-colorblind', 'seaborn-talk', 'grayscale', 'seaborn-dark-palette', 'seaborn-dark', 'bmh', 'seaborn-deep', 'seaborn', 'seaborn-whitegrid', 'seaborn-muted']

    #plt.figure() 
    #data_frame.plot(x='learning evaluation instances')

    #font = {'family' : 'normal', 'weight' : 'bold', 'size'   : 24}
    #font = {'size'   : 24}
    #matplotlib.rc('font', **font)
    #plt.rcParams.update({'font.size': 20})
    ax = data_frame.plot(figsize=(18,6))
    ax.set_ylabel('Error rate', fontsize=20)
    ax.set_xlabel('Instances', fontsize=20)
    ax.xaxis.label.set_size(20)
    ax.set_ylim([0.0, 1.0])
    ax.set_facecolor((1.0, 1.0, 1.0))
    ax.tick_params(labelsize=20)
    legend = ax.legend(loc=1, fancybox=True, prop={'size': 20}) #loc = upper right
    legend.get_frame().set_alpha(0.1)
    #ax2 = ax
    if df_aux is not None:
      ax2 = ax.twinx()
      ax2 = df_aux.plot(kind='area', ax=ax2, alpha=0.25, secondary_y=False)
      ax2.set_ylabel('Splits', fontsize=20)
      ax2.tick_params(labelsize=20)
      ax2.set_yticks(np.arange(0,max(3, df_aux['splits'].max()+1),1))
      legend2 = ax2.legend(loc=2, fancybox=True, prop={'size': 20}) #loc = upper right
      legend2.get_frame().set_alpha(0.1)
    #ax.set_facecolor((0.94, 0.999, 0.999))

   # Print the last of the commands used     
    #ax.set_xlim([0.0, evl.num_instances])
    wrapped_cmd = '\n'.join(wrap(cmd, 100))
    #ax.text(0.0, 1.025, wrapped_cmd, bbox=dict(facecolor='green', alpha=0.2), transform=ax.transAxes, zorder=100)
    #ax.text(0.93, 0.98, r'Drift Magnitude', bbox=dict(facecolor='blue', alpha=0.2), transform=ax.transAxes, zorder=100)
    #ax.text(-0.03, -0.1, r'|Error Curves|', bbox=dict(facecolor='white', alpha=0.3), transform=ax.transAxes, zorder=100)
    #ax.text(left, top, wrapped_cmd, bbox=dict(facecolor='green', alpha=0.3), transform=ax.transAxes, zorder=100)

    #figure = plt.figure()
    figure = ax2.get_figure()


    #plt.annotate(fontsize=1)

    figure.savefig(figPath+'.png', bbox_inches='tight')
    #plt.show()




class CompositeExperimentSuiteRunner:

  #learners = report0
  learners = listOfLearners.vfdt_decay
  #learners = learners_1

  @classmethod
  def runExperimentSuite(cls):
    utilities.remove_folder(mcv.FIG_DIR)
    utilities.make_folder(mcv.FIG_DIR)

    i = 0

    #for learnerBuilder in cls.learnerBuilders:
    #  CompositeExperimentRunner.runExperiments(learnerBuilder(), i)
    #  i+=1

    for learner in cls.learners:
      CompositeExperimentRunner.runExperiments(lrn.Learner(learner), i)
      i+=1


# Composite of many instances of a given experiment running in parallel. 
# Note that the seed for the random generator must change!
# Multiple stream Processes for an experiment
class CompositeExperimentRunner:

  processes = [] 

  @classmethod
  def runExperiments(this, learner, figNo):
    output_files = []

    os.chdir(mcv.MOA_DIR)
    utilities.remove_folder(mcv.OUTPUT_DIR)
    utilities.make_folder(mcv.OUTPUT_DIR)

    #evaluator = evl.EvaluatorBuilder.EvaluatePrequentialAdwinBuilder()
    evaluator = evl.EvaluatorBuilder.EvaluatePrequentialBuilder()

    gen_strings_abrupt_conditional = [
            r"generators.monash.AbruptDriftGenerator  -n 4 -v 4 -b 9999999  -o 0.2  -c  -r 0 ",
            r"generators.monash.AbruptDriftGenerator  -n 4 -v 4 -b 100000  -o 0.3  -c  -r 0 ",
            r"generators.monash.AbruptDriftGenerator  -n 4 -v 4 -b 100000  -o 0.5  -c  -r 0 ",
            r"generators.monash.AbruptDriftGenerator  -n 4 -v 4 -b 100000  -o 0.8  -c  -r 0 ",
            ]

    gen_strings_recurrent = [
            #r"ConceptDriftStream -s (generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.700002 -c -n 4 -v 4 -r 1 -b 1) -p 200000 -w 2000 -r 1"
            #r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.8 -c -n 4 -v 4 -r 1 -b 1) -w 4000",
            #r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.5 -c -n 4 -v 4 -r 1 -b 1) -w 4000",
            #r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.3 -c -n 4 -v 4 -r 1 -b 1) -w 4000",
            #r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.1 -c -n 4 -v 4 -r 1 -b 1) -w 4000"
            ]

    gen_strings_square_wave = [
            r"RecurrentConceptDriftStream -x 100000 -y 100000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -z 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.75 -c -n 4 -v 4 -z 4 -r 1 -b 0) -w 50000 -p 150000",
            r"RecurrentConceptDriftStream -x 100000 -y 100000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -z 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.5 -c -n 4 -v 4 -z 4 -r 1 -b 0) -w 50000 -p 150000",
            r"RecurrentConceptDriftStream -x 100000 -y 100000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -z 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.25 -c -n 4 -v 4 -z 4 -r 1 -b 0) -w 50000 -p 150000",
            r"RecurrentConceptDriftStream -x 100000 -y 100000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -z 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.0 -c -n 4 -v 4 -z 4 -r 1 -b 0) -w 50000 -p 150000"
        ]


    gen_strings_exp_2_2 = [
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 3 -b 9999999 -o 0.0",
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 3 -b 150000 -o 0.25",
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 3 -b 150000 -o 0.5",
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 3 -b 150000 -o 0.75"
        ]

    gen_strings_exp_3_3 = [
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -z 3 -r 1 -b 999999 -o 0.0",
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -z 3 -r 1 -b 150000 -o 0.25",
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -z 3 -r 1 -b 150000 -o 0.5",
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -z 3 -r 1 -b 150000 -o 0.75"
        ]

    gen_strings_exp_4_4 = [
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 9999999 -o 0.0",
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 150000 -o 0.3",
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 150000 -o 0.5",
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 150000 -o 0.8"
        ]

    gen_strings_gradual = [
            #r"ConceptDriftStream -p 200000 -w 100000 -s (generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 1 -b 99999999 -o 0.8) -d (generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 1 -b 1 -o 0.8)"
            #r"ConceptDriftStream -p 200000 -w 100000 -s (generators.monash.AbruptDriftGenerator -c -z 2 -r 1 -b 99999999 -o 0.8) -d (generators.monash.AbruptDriftGenerator -c -z 2 -r 1 -b 1 -o 0.8)"
            r"ConceptDriftStream -s (generators.monash.AbruptDriftGenerator -o 0.75 -c -n 2 -v 2 -z 2 -r 1 -b 999999) -d (generators.monash.AbruptDriftGenerator -o 0.75 -c -n 2 -v 2 -z 2 -r 1 -b 1) -p 150000 -w 20000 -r 1",
            r"ConceptDriftStream -s (generators.monash.AbruptDriftGenerator -o 0.50 -c -n 2 -v 2 -z 2 -r 1 -b 999999) -d (generators.monash.AbruptDriftGenerator -o 0.5 -c -n 2 -v 2 -z 2 -r 1 -b 1) -p 150000 -w 20000 -r 1",
            r"ConceptDriftStream -s (generators.monash.AbruptDriftGenerator -o 0.25 -c -n 2 -v 2 -z 2 -r 1 -b 999999) -d (generators.monash.AbruptDriftGenerator -o 0.25 -c -n 2 -v 2 -z 2 -r 1 -b 1) -p 150000 -w 20000 -r 1",
            r"ConceptDriftStream -s (generators.monash.AbruptDriftGenerator -o 0.0 -c -n 2 -v 2 -z 2 -r 1 -b 999999) -d (generators.monash.AbruptDriftGenerator -o 0.0 -c -n 2 -v 2 -z 2 -r 1 -b 1) -p 150000 -w 20000 -r 1",
        ]

#EvaluatePrequential -l trees.HATADWIN -s (ConceptDriftStream -s (generators.RandomTreeGenerator -r 2 -i 2 -u 0) -d (generators.RandomTreeGenerator -r 3 -i 3 -u 0) -p 200000 -w 10 -r 20) -i 400000 -f 1000
    #gen_strings = gen_strings_abrupt_conditional
    #gen_strings = gen_strings_exp_1_4
    #gen_strings = gen_strings_square_wave
    #gen_strings = gen_strings_MOA_TREE
    #gen_strings = gen_strings_exp_2_2 #Use for showing VFDT bug in paper_amnesia
    #gen_strings = gen_strings_exp_2_2
    gen_strings = gen_strings_exp_3_3
    #gen_strings = gen_strings_gradual

    seeded_exp = CompositeExperimentBuilder.seededExpBuilder(mcv.NUM_STREAMS, mcv.OUTPUT_DIR, mcv.OUTPUT_PREFIX, this.processes, evaluator, learner, gen_strings)
    #seeded_exp = CompositeExperimentBuilder.seededExpBuilderMOATREE(mcv.NUM_STREAMS, mcv.OUTPUT_DIR, mcv.OUTPUT_PREFIX, this.processes, evaluator, learner, gen_strings)
    #prior_drift_mag_exp = CompositeExperimentBuilder.varyPriorDriftMagBuilder(mcv.NUM_STREAMS, mcv.OUTPUT_DIR, mcv.OUTPUT_PREFIX, this.processes, evaluator, learner)
    #conditional_drift_mag_exp = CompositeExperimentBuilder.varyConditionalDriftMagBuilder(mcv.NUM_STREAMS, mcv.OUTPUT_DIR, mcv.OUTPUT_PREFIX, this.processes, evaluator, learner)

    #for exp in prior_drift_mag_exp.getExperiments():
    #for exp in conditional_drift_mag_exp.getExperiments():
    for exp in seeded_exp.getExperiments():
      exp.run(this.processes)
      # Run experiments setting output files

    exit_codes = [p.wait() for p in this.processes]
    # wait until all experiments have finished running: each experiment corresponds to a process.


    #output_files = prior_drift_mag_exp.getOutputFiles()
    #output_files = conditional_drift_mag_exp.getOutputFiles()
    output_files_u = seeded_exp.getOutputFiles() #this is dict, it's unsorted, this messes up colors in plots
    output_files = OrderedDict(sorted(output_files_u.items(), key = lambda t: t[0])) # sort entries by key

    #for key in output_files:
    #  print("====" + str(key) + str(output_files[key]))

    # List of mean_dataframes
    mean_dataframes = []
    # Dataframe that contains all the mean error columns for the experiments
    error_df = pd.DataFrame([])
    # Dataframe that contains all the mean split columns for the experiments
    split_df = pd.DataFrame([])

    # Load the outputs into dataframes to prepare for averaging
    # output_files is a 2D list. It has a folder-file structure.
    for folder, files in output_files.items(): 
      # List of dataframes in this folder
      dataframes = []
      for this_file in files:
        #dataframes.append(pd.read_csv(this_file, index_col=False, header=0, skiprows=prior_drift_mag_exp.getSkipRows()))
        #dataframes.append(pd.read_csv(this_file, index_col=False, header=0, skiprows=conditional_drift_mag_exp.getSkipRows()))
        print("====" + this_file) 
        dataframes.append(pd.read_csv(this_file, index_col=False, header=0, skiprows=seeded_exp.getSkipRows()))

        # index_col has to be False as col 0 isn't integer

      # Concatenate all of these. This creates a very large file
      # In order to be memory efficient, maybe just add values from other files into one file
      all_stream_learning_data = pd.concat(dataframes)
      #all_stream_learning_data.to_csv(folder_file_prefix + "Cumulative.csv")
  
      all_stream_mean = {}
      # average row by row
      int_evl_num_rows = int(evl.NUM_ROWS) #for python 3
      for i in range(int_evl_num_rows): 
        all_stream_mean[i] = all_stream_learning_data[i::int_evl_num_rows].mean()
  
      all_stream_mean_df = pd.DataFrame(all_stream_mean).transpose() 
      #all_stream_mean_df.to_csv(folder_file_prefix + "Mean.csv")

      all_stream_mean_df['error'] = (100.0 - all_stream_mean_df['classifications correct (percent)'])/100.0

      # Only mark actual splits as 1 and discard the rest of the split counts
      splitArray = all_stream_mean_df['splits']
      i = 0
      while i < splitArray.size-1:
        #print(str(i+1) + " " + str(splitArray[i+1]) + "\n")
        diff = math.floor(splitArray[i+1]) - math.floor(splitArray[i])
        if(diff > 0):
          splitArray[i+1] = (-1)*diff
          i = i+2
        else:
          i=i+1
      for i in range(splitArray.size):
        if(splitArray[i] > 0):
          splitArray[i] = 0
        else:
          splitArray[i] = (-1) * splitArray[i] 

      #splitArray should just be a name bound to the object that was changed, the column of the data_frame
      # There should be no reason to assign back
      all_stream_mean_df['splits'] = splitArray
      # these should both be already bound to the same object...

      #all_stream_mean_df["splits"] = all_stream_mean_df['splits']/all_stream_mean_df['splits'].iloc[int_evl_num_rows-1]
      # each split count is divided by the end-of-learning split count in order to normalize to 1

      # Add this folder's mean error column to the error_df 
      #error_df[str(folder)] = all_stream_mean_df['error'] 
      average_error = all_stream_mean_df['error'].sum()/int_evl_num_rows
      cpu_time = all_stream_mean_df['evaluation time (cpu seconds)'].iloc[int_evl_num_rows-1] # yes this is avg cpu_time
      #print("+++++++++++" + str(jkl))
      error_df[" M: "+ str(folder)+ " | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      split_df["splits"] = all_stream_mean_df['splits']
      #error_df[str(folder)+" "+"5"] = all_stream_mean_df['error']

      mean_dataframes.append(all_stream_mean_df)

    # Set the index column
    # error_df[mcv.INDEX_COL]
    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    error_df = error_df.set_index(mcv.INDEX_COL)
    error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

    split_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    split_df = split_df.set_index(mcv.INDEX_COL)
    split_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Split.csv")

    # Plot.plot_df(all_stream_mean_df)
    Plot.plot_df(error_df, exp.getCmd(), mcv.FIG_DIR+"/"+str(figNo), split_df)

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

  def getCmd(self):
    return self.cmd

class ExperimentBuilder:

  @staticmethod
  def buildExp(output_file, processes, evaluator, learner, generator):
    e = Experiment(mcv.MOA_STUMP, evaluator, learner, generator, evl.PARAMS, output_file, processes)
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
  def varyPriorDriftMagBuilder(num_streams, output_folder, file_prefix, processes, evaluator, learner):
    skip_rows = 0
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
        generator = gen.GeneratorBuilder.MonashAbruptDriftGenBuilder(nAttributes=2, nValuesPerAttribute=2, burnIn=100000000, driftMagPrior=drift_mag, driftPrior=True, randomSeed=i+1)
	# Same seed for each stream index across magnitudes
        output_file = folder_file_prefix + str(i) + '.csv'
        this_folder_output_files.append(output_file)
        exp_list.append(ExperimentBuilder.PriorDriftMagBuilder(output_file, processes, evaluator, learner, generator))

      output_files[drift_mag] = this_folder_output_files

    return CompositeExperiment(exp_list, output_files, skip_rows)


  @staticmethod
  def varyConditionalDriftMagBuilder(num_streams, output_folder, file_prefix, processes, evaluator, learner):
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

      #generator = gen.GeneratorBuilder.CategoricalAbruptDriftGenBuilder(nAttributes=3, nValuesPerAttribute=5, burnIn=100000, driftMagConditional=drift_mag, driftConditional=True)

      for i in range(0, num_streams):
        generator = gen.GeneratorBuilder.MonashAbruptDriftGenBuilder(nAttributes=4, nValuesPerAttribute=4, burnIn=100000, driftMagConditional=drift_mag, driftConditional=True, randomSeed=i+5)
        output_file = folder_file_prefix + str(i) + '.csv'
        this_folder_output_files.append(output_file)
        exp_list.append(ExperimentBuilder.ConditionalDriftMagBuilder(output_file, processes, evaluator, learner, generator))

      output_files[drift_mag] = this_folder_output_files

    return CompositeExperiment(exp_list, output_files, skip_rows)


  # As of now I won't have a list of experiments, so just one folder for multiple seeded runs of same exp.
  # Change this to add a list of experiments.
  @staticmethod
  def seededExpBuilder(num_streams, output_folder, file_prefix, processes, evaluator, learner, gen_strings):
    skip_rows = 2
    exp_list = []
    output_files = {}

    exp_no = 0
    for gen_string in gen_strings:
      exp_no+=1
      this_output_folder = output_folder + '/' + str(exp_no)
      folder_file_prefix = this_output_folder + '/' + file_prefix
      utilities.remove_folder(this_output_folder)
      utilities.make_folder(this_output_folder)
      this_folder_output_files = []

      for i in range(0, num_streams):
        generator = gen.GeneratorBuilder.SimpleSeededGenBuilder(gen_string, randomSeed=i+2)
        # give as input a generator seeded with 0. We then increment the seed. This works for our purposes.
        output_file =  folder_file_prefix +  str(i) + '.csv'
        this_folder_output_files.append(output_file)
        exp_list.append(ExperimentBuilder.buildExp(output_file, processes, evaluator, learner, generator))

# best place to provide a legend... the index becomes the legend
      legend = re.search(r"-o (0\.\d+)", gen_string)
      output_files[legend.group(1)] = this_folder_output_files

    return CompositeExperiment(exp_list, output_files, skip_rows)


  @staticmethod
  def seededExpBuilderMOATREE(num_streams, output_folder, file_prefix, processes, evaluator, learner, gen_strings):
    skip_rows = 2
    exp_list = []
    output_files = {}

    exp_no = 0
    for gen_string in gen_strings:
      exp_no+=1
      this_output_folder = output_folder + '/' + str(exp_no)
      folder_file_prefix = this_output_folder + '/' + file_prefix
      utilities.remove_folder(this_output_folder)
      utilities.make_folder(this_output_folder)
      this_folder_output_files = []

      for i in range(0, num_streams):
        generator = gen.GeneratorBuilder.SimpleSeededGenBuilderMOATREE(gen_string, randomSeed=i+2)
        # give as input a generator seeded with 0. We then increment the seed. This works for our purposes.
        output_file =  folder_file_prefix +  str(i) + '.csv'
        this_folder_output_files.append(output_file)
        exp_list.append(ExperimentBuilder.buildExp(output_file, processes, evaluator, learner, generator))

      output_files[exp_no] = this_folder_output_files

    return CompositeExperiment(exp_list, output_files, skip_rows)


