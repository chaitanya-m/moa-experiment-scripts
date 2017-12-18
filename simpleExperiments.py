
import os, subprocess, shlex, shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import pylab
import numpy as np

import re
import utilities
import math
import moa_command_vars as mcv
from textwrap import wrap
from collections import OrderedDict

import listOfLearners

# Most operations are built around directories of csv files
# files are named with simple numbers and this is important for sorting

class Plot:
  # Assumption: Received data contains a correctly computed error column 

  #def __init__(self):

  @staticmethod
  def plot_df(data_frame, cmd, figPath, df_aux = None):

   # matplotlib.rcParams.update({'font.size': 24})
    # theres a whole bunch of available styles
    matplotlib.style.use('seaborn-paper')
#   styles = ['seaborn-darkgrid', 'seaborn-white', 'fivethirtyeight', 'seaborn-bright', 'seaborn-pastel', 'ggplot', 'classic', 'seaborn-notebook', '_classic_test', 'seaborn-ticks', 'seaborn-poster', 'dark_background', 'seaborn-paper', 'seaborn-colorblind', 'seaborn-talk', 'grayscale', 'seaborn-dark-palette', 'seaborn-dark', 'bmh', 'seaborn-deep', 'seaborn', 'seaborn-whitegrid', 'seaborn-muted']

    ax = data_frame.plot(figsize=(18,6))
    ax.set_ylabel('Error rate', fontsize=27)
    ax.set_xlabel('Instances (x 1,000)', fontsize=27)
    ax.xaxis.label.set_size(27)
    ax.set_ylim([0.0, 1.0])
    ax.set_facecolor((1.0, 1.0, 1.0))
    ax.tick_params(labelsize=27)
    legend = ax.legend(loc=1, fancybox=True, prop={'size': 27}) #loc = upper right
    legend.get_frame().set_alpha(0.1)

    ax2 = ax
    if df_aux is not None:
      ax2 = ax.twinx()
      ax2 = df_aux.plot(kind='area', ax=ax2, alpha=0.27, secondary_y=False)
      ax2.set_ylabel('Splits', fontsize=27)
      ax2.tick_params(labelsize=27)
      ax2.set_yticks(np.arange(0,max(3, df_aux['splits'].max()+1),1))
      legend2 = ax2.legend(loc=2, fancybox=True, prop={'size': 27}) #loc = upper right
      legend2.get_frame().set_alpha(0.1)

   # Print the last of the commands used     
    wrapped_cmd = '\n'.join(wrap(cmd, 100))

    figure = ax2.get_figure()

    figure.savefig(figPath+'.png', bbox_inches='tight')

learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
generators = [
        # show that increasing the number of classes favors EFDT
  r"-s (ArffFileStream -f /home/mchait/Downloads/hepmass.arff -c 1)"
  #r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 2 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
  #r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 3 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
  #r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 4 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
  #r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 5 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
  ]
evaluators = [ r"EvaluatePrequential -i 70000 -f 1000 -q 1000"]


class Experiment:

  def __init__(self, stump, e, l, g):
    self.cmd = " ".join([stump, "moa.DoTask",  e, l, g])
        
  @staticmethod 
  def make_running_process(exp, output_file):
    
    args = shlex.split(exp.cmd)
    process = subprocess.Popen(args, stdout=open(output_file, "w+"))
    return process


class CompositeExperiment:

  @staticmethod
  def make_experiments(stump, evaluators, learners, generators):

    experiments = []

    for evaluator in evaluators:  
      for learner in learners:
        for generator in generators:
          experiments.append(Experiment(stump, evaluator, learner, generator))

    return experiments

  @staticmethod
  def make_running_processes(experiments, output_dir):

    os.chdir(mcv.MOA_DIR)
    utilities.remove_folder(output_dir)
    utilities.make_folder(output_dir)

    processes = []
    output_files = []

    counter = 0
    for exp in experiments:
      output_file = output_dir + '/' + str(counter)
      process = Experiment.make_running_process(exp, output_file)
      processes.append(process)
      counter+=1

    return processes


class Utils: 

  @staticmethod
  def file_to_dataframe(some_file):
    return pd.read_csv(some_file, index_col=False, header=0, skiprows=0)

  @staticmethod
  def dataframe_to_file(some_dataframe, output_csv):
    return some_dataframe.to_csv(some_file, output_csv)

  @staticmethod
  def wait_for_processes(processes):
    exit_codes = [p.wait() for p in processes] #waits for all processes to terminate

  @staticmethod
  def error_df_from_folder(folder):
    error_df = pd.DataFrame([])  
    files = sorted(os.listdir(folder))
    for filename in files:
      file_df = Utils.file_to_dataframe(folder+'/'+filename)
      error_df[str(filename)] = (100.0 - file_df['classifications correct (percent)']) / 100.0

    return error_df

  @staticmethod
  def runtime_dict_from_folder(folder):
    runtimes = {}
    files = sorted(os.listdir(folder))
    for filename in files:
      file_df = Utils.file_to_dataframe(folder+'/'+filename)
      runtimes[filename] = file_df['evaluation time (cpu seconds)'].iloc[-1]

    return runtimes


def test():
    output_dir = mcv.OUTPUT_DIR
    experiments = CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, learners, generators)
    processes = CompositeExperiment.make_running_processes(experiments, output_dir)
    Utils.wait_for_processes(processes)

    error_df = Utils.error_df_from_folder(output_dir)
    runtime_dict = Utils.runtime_dict_from_folder(output_dir)

    new_col_names = ["VFDT", "EFDT"]
    for col in error_df.columns:
        new_col_names[int(col)] = (str(col)+ ": "+ new_col_names[int(col)] + " | T:" + ("%.2f s"%runtime_dict[col]) + " | E: " + ("%.6f"%error_df[col].mean()))
    error_df.columns = new_col_names

    Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(1).zfill(3))



    # without the main sentinel below code will always get run, even when imported as a module!
if __name__=="__main__": 
    test()

