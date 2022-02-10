
import matplotlib
matplotlib.use('Agg') # so you don't call a display over ssh

import os, subprocess, shlex, shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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


class Generator:

    def __init__(self, command):
        self.command = command
    def cmd(self):
        return self.command

class Plot:
  # Assumption: Received data contains a correctly computed error column 

  #def __init__(self):

  @staticmethod
  def plot_df(caption,data_frame, cmd, figPath, df_aux = None, df_end = None, df_avg = None):

    data_frame = data_frame.round(4)

    if df_aux is not None:
        df_aux = df_aux.round(4)
    if df_end is not None:
        df_end = df_end.round(4)
    if df_avg is not None:
        df_avg = df_avg.round(4)


   # matplotlib.rcParams.update({'font.size': 24})
    # theres a whole bunch of available styles
    matplotlib.style.use('seaborn-ticks')
#   styles = ['seaborn-darkgrid', 'seaborn-white', 'fivethirtyeight', 'seaborn-bright', 'seaborn-pastel', 'ggplot', 'classic', 'seaborn-notebook', '_classic_test', 'seaborn-ticks', 'seaborn-poster', 'dark_background', 'seaborn-paper', 'seaborn-colorblind', 'seaborn-talk', 'grayscale', 'seaborn-dark-palette', 'seaborn-dark', 'bmh', 'seaborn-deep', 'seaborn', 'seaborn-whitegrid', 'seaborn-muted']

    linestyles = ['-.', ':', '-', '--', ':', ':', '-', '-.', '--', ':']
    linewidths = [6, 3, 4, 2, 1.5, 2, 1, 1, 2, 1.5]
    dashes = [[4,3], [3,1], [4,1,1,1], [1, 1], [], [3,1], [2,1,2,1], [], [4,1,2,1], [3,1]]
    alphas = [0.7, 0.9, 0.9, 0.8, 0.8, 1.0, 1.0, 1.0, 0.9, 0.8]
    colors = ['green','black','red','blue', 'magenta', 'cyan','lime','gray','maroon','fuchsia']
    cellHeight = 0.057
    headerHeight = 0.2

    fig = plt.figure(figsize=(24, 36))
    fig.text(0.5,0.9, caption, ha='center', fontsize=50)
    gs = gridspec.GridSpec(nrows=3, ncols=1, height_ratios=[1.3,1,1.1])
    gs.update(hspace=0.25)

    ax = fig.add_subplot(gs[0])
    if df_avg is not None:
      ax3 = fig.add_subplot(gs[1])
    if df_end is not None:
      ax4 = fig.add_subplot(gs[2])

    data_frame.plot(style=linestyles, ax = ax)
#   use this as necessary
    for i, l in enumerate(ax.lines):
      plt.setp(l, linewidth=linewidths[i])
      l.set_dashes(dashes[i]) #override linestyles
      l.set_alpha(alphas[i])
      l.set_color(colors[i])

    #ax.set_yscale("log")
    ax.set_ylabel('Error rate', fontsize=44)
    ax.set_xlabel('Instances (x 1,000)', fontsize=44)
    ax.xaxis.label.set_size(44)
    ax.set_ylim([0.0, 1.0])
    ax.set_xlim([0.0, 200])
    ax.set_facecolor((1.0, 1.0, 1.0))
    ax.tick_params(labelsize=44)
    
    #legend = ax.legend(loc=1, fancybox=True, prop={'size': 22}, frameon=True) #loc = upper right
    # use above for papers

    labels = [ '\n'.join(wrap(l, 50)) for l in data_frame.columns]
    #labels = ["VFDT                     E: 0.3368 | T: 2.51 s" , "VFDT Unforgetting E: 0.5782 | T: 2.41 s"]
    legend = ax.legend(labels, loc='upper right', #bbox_to_anchor=(0.5, 1.15),
            fancybox=True, shadow=True, ncol=1, prop = {'size': 36}) # this one for thesis
    legend.get_frame().set_color((1.0,1.0,1.0))
    legend.get_frame().set_alpha(0.7)

    ax2 = ax
    if df_aux is not None:
      ax2 = ax.twinx()
      ax2 = df_aux.plot(style=['-',':'], kind='line', ax=ax2, alpha = 0.8, secondary_y=False)
      ax2.set_ylabel('Splits', fontsize=44)
      ax2.tick_params(labelsize=22)
      if df_aux.values.max() <= 10:
        ax2.set_yticks(np.arange(0,max(3, df_aux.values.max()+1),1))
      else:
        ax2.set_yticks(np.arange(0,max(3, df_aux.values.max()+1),3))
	
      legend2 = ax2.legend(loc=2, fancybox=True, prop={'size': 44}) #loc = upper right
      legend2.get_frame().set_alpha(0.1)

   # Print the last of the commands used     
    wrapped_cmd = '\n'.join(wrap(cmd, 100))

    if df_end is not None:
      ax4.xaxis.set_visible(False) 
      ax4.yaxis.set_visible(False)
      ax4.axis("off")
      ax4.set_title("Endpoint Averages\n", fontsize=52)
      table_end = ax4.table(cellText=df_end.values,
              colLabels=[x[:3] for x in df_end.columns], 
              #colLabels=[str(x+1) for x in range(len(df_end.columns))], 
              rowLabels=list(df_end.index),loc='center')
      table_end.auto_set_font_size(False)
      table_end.set_fontsize(36)
  
  # the row labels column is... -1 !! But col labels row is 0.
  # This really really messes up indexing
      cellDict = table_end.get_celld()
      for i in range(1, len(df_end)+1):
          for j in range(0,len(df_end.columns)):
              cellDict[(i,j)].set_height(cellHeight)
      for i in range(1,len(df_end)+1):
          cellDict[(i,-1)].set_height(cellHeight)
      for j in range(0,len(df_end.columns)):
          cellDict[(0,j)].set_height(headerHeight)
  
      #df_end.plot(table=True, ax = ax4)
      
    if df_avg is not None:
      ax3.xaxis.set_visible(False) 
      ax3.yaxis.set_visible(False)
      ax3.axis("off")
      ax3.set_title("Averages of Averages", fontsize=52)
      table_avg = ax3.table(cellText=df_avg.values,
              colLabels=[x[:3] for x in df_avg.columns], 
              #colLabels=["\n".join(wrap(x)) for x in df_avg.columns], 
              #colLabels=[str(x+1) for x in range(len(df_avg.columns))], 
              rowLabels=list(df_avg.index),loc='center')
      table_avg.auto_set_font_size(False)
      table_avg.set_fontsize(36)
  
      cellDict = table_avg.get_celld()
      for i in range(1, len(df_avg)+1):
          for j in range(0,len(df_avg.columns)):
              cellDict[(i,j)].set_height(cellHeight)
      for i in range(1,len(df_avg)+1):
          cellDict[(i,-1)].set_height(cellHeight)
      for j in range(0,len(df_avg.columns)):
          cellDict[(0,j)].set_height(headerHeight)
  
      #figure = ax2.get_figure()
  
      #gs.tight_layout(fig, w_pad=0.1)
      #plt.tight_layout()
  
    fig.savefig(figPath+'.png', bbox_inches='tight')
  
      #print df_end
  
      #ax = plt.subplot(111, frame_on=False) # no visible frame
      #ax.xaxis.set_visible(False)  # hide the x axis
      #ax.yaxis.set_visible(False)  # hide the y axis
  
      #table(ax, df_end)  # where df is your data frame
  
      #plt.savefig(figPath+'table.png', bbox_inches='tight')
  

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
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    processes = []
    output_files = []

    counter = 0
    for exp in experiments:
      output_file = output_dir + '/' + str(counter)
      process = Experiment.make_running_process(exp, output_file)
      processes.append(process)
      counter+=1

    return processes

  @staticmethod
  def SimpleSeededGenBuilder(gen_string, randomSeed=None):

    # if random seed is not none, just substitute any -r options with the correct seed
    # the -r options must be clearly visible... 
    # imagine the amount of refactoring needed every time new options are added... that's too
    # much complexity for a piece of code custom-built to work with MOA.

    gen_cmd = " -s \"\"\"(" + re.sub("-r [0-9]+", "-r "+ str(randomSeed)+ " ", str(gen_string)) + " )\"\"\""

    return Generator(gen_cmd)

  @staticmethod
  def multiSeededGenBuilder(gen_string, randomSeed=None):
    # ASSUMPTION: NO MORE THAN 100,000 STREAMS

    max_streams = 100000

    rand_opt = "-r [0-9]+"
    #find locations of -r option occurrences
    occurence_locs = [m.start() for m in re.finditer(rand_opt, gen_string)]
    occ = 0
    for i in occurence_locs:
      occ += 1  
      # split before and after the i'th rand_opt occurrence  
      before = gen_string[:i]
      after = gen_string[i:]
      after = re.sub("-r [0-9]+", "-r "+ str(int(randomSeed)+int(occ)*max_streams), after, 1)
      # update string and move on to next rand_opt
      gen_string = before + after


    rand_opt = "-i [0-9]+"
    #find locations of -r option occurrences
    occurence_locs = [m.start() for m in re.finditer(rand_opt, gen_string)]
    occ = 0
    for i in occurence_locs:
      occ += 1  
      # split before and after the i'th rand_opt occurrence  
      before = gen_string[:i]
      after = gen_string[i:]
      after = re.sub("-i [0-9]+", "-i "+ str(int(randomSeed)+int(occ)*max_streams), after, 1)
      
      # update string and move on to next rand_opt
      gen_string = before + after

    gen_cmd = str(gen_string)
    return gen_cmd


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


  @staticmethod
  def end_stats_from_folder(folder):

    fieldTokens = mcv.FIELDS.split(',')
    dict_of_dicts = {}
    for field in fieldTokens:
        dict_of_dicts[field] = dict()
    files = sorted(os.listdir(folder))
    for filename in files:
      file_df = Utils.file_to_dataframe(folder+'/'+filename)
      for field in dict_of_dicts.keys():
        dict_of_dicts[field][filename] = file_df[field].iloc[-1]

    return dict_of_dicts


  @staticmethod
  def split_df_from_folder(folder):
    split_df = pd.DataFrame([])  
    files = sorted(os.listdir(folder))
    for filename in files:
      file_df = Utils.file_to_dataframe(folder+'/'+filename)

      # Only mark actual splits as 1 and discard the rest of the split counts
      splitArray = file_df.loc[:,'splits'].values.tolist()
      i = 0
      while i < len(splitArray)-1:
        #print(str(i+1) + " " + str(splitArray[i+1]) + "\n")
        diff = math.floor(splitArray[i+1]) - math.floor(splitArray[i])
        if(diff > 0):
          splitArray[i+1] = (-1)*diff
          i = i+2
        else:
          i=i+1
      for i in range(len(splitArray)):
        if(splitArray[i] > 0):
          splitArray[i] = 0
        else:
          splitArray[i] = (-1) * splitArray[i]
      split_df[str(filename)] = splitArray

    return split_df

"""
learning evaluation instances,evaluation time (cpu seconds),model cost (RAM-Hours),classified instances,classifications correct (percent),Kappa Statistic (percent),Kappa Temporal Statistic (percent),Kappa M Statistic (percent),model training instances,model serialized size (bytes),tree size (nodes),tree size (leaves),active learning leaves,tree depth,active leaf byte size estimate,inactive leaf byte size estimate,byte size estimate overhead,splits
"""

