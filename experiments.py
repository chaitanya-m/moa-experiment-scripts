
import os, subprocess, shlex, shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import pylab

import re
import utilities
import generators as gen
import learners as lrn
import evaluators as evl
import moa_command_vars as mcv
from textwrap import wrap
from collections import OrderedDict

class Plot:
  # Assumption: Received data contains a correctly computed error column 

  #def __init__(self):

  @staticmethod
  def plot_df(data_frame, cmd, figPath):
    matplotlib.style.use('ggplot')
    #plt.figure() 
    #data_frame.plot(x='learning evaluation instances')
    ax = data_frame.plot(figsize=(20,5))
    ax.set_ylabel('Error rate')
    ax.set_ylim([0.0, 1.0])
    
    #ax.set_xlim([0.0, evl.num_instances])
    wrapped_cmd = '\n'.join(wrap(cmd, 140))
    ax.text(-0.03, 0.95, wrapped_cmd, bbox=dict(facecolor='green', alpha=0.3), transform=ax.transAxes, zorder=100)
    #ax.text(0.93, 0.98, r'Drift Magnitude', bbox=dict(facecolor='blue', alpha=0.2), transform=ax.transAxes, zorder=100)
    ax.text(-0.03, -0.05, r'[Error Curves]', bbox=dict(facecolor='white', alpha=0.3), transform=ax.transAxes, zorder=100)
    #ax.text(left, top, wrapped_cmd, bbox=dict(facecolor='green', alpha=0.3), transform=ax.transAxes, zorder=100)
    figure = ax.get_figure()
    figure.savefig(figPath+'.png')
    #plt.show()



class CompositeExperimentSuiteRunner:

  learnerBuilders = [
                      #lrn.LearnerBuilder.NaiveBayesLearnerBuilder, 
                      lrn.LearnerBuilder.DecisionStumpLearnerBuilder,
                      lrn.LearnerBuilder.HoeffdingAdaptiveLearnerBuilder,
                      #lrn.LearnerBuilder.HoeffdingOptionLearnerBuilder,
                      lrn.LearnerBuilder.HoeffdingLearnerBuilder,
                      #lrn.LearnerBuilder.OzaBagLearnerBuilder,
                      lrn.LearnerBuilder.OzaBoostLearnerBuilder,
                      #lrn.LearnerBuilder.AccuracyUpdatedEnsembleLearnerBuilder,
                      #lrn.LearnerBuilder.AccuracyWeightedEnsembleLearnerBuilder,
                      #lrn.LearnerBuilder.DriftDetectionMethodClassifierLearnerBuilder,
                      #lrn.LearnerBuilder.OzaBagAdwinLearnerBuilder,
                      #lrn.LearnerBuilder.OzaBoostAdwinLearnerBuilder,
                      #lrn.LearnerBuilder.HoeffdingAdaptiveLearnerBuilder
                      ] 

  learners_1 = [
                r"-l trees.HoeffdingTree",
                r"-l (trees.HoeffdingTree -g 100 -c 0.01)",
            ]
  learners_2 = [
                r"-l trees.HoeffdingTree",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree)",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINChangeDetector)",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d SeqDrift2ChangeDetector)"
                ]
  
  learners_2_1 = [
                r"-l trees.EFDT",
                r"-l trees.HoeffdingTree",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree)",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINChangeDetector)", 
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINMonotoneChangeDetector)",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d SeqDrift2ChangeDetector)",
                r"-l trees.HoeffdingAdaptiveTree",
                r"-l trees.HoeffdingOptionTree"
                ]

  learners_3_1 = [
                #r"-l trees.EFDT",
                r"-l trees.HoeffdingTree",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree)",
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINMonotoneChangeDetector)",
                r"-l trees.HoeffdingAdaptiveTree",
                #r"-l trees.HoeffdingOptionTree"
                ]
 
  temp = [
                r"-l (meta.OzaBoost -l (trees.HoeffdingTree -g 100 -c 0.01))",
                r"-l meta.AccuracyUpdatedEnsemble",

                r"-l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01)",
                r"-l (meta.OzaBoost -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.1)) ",
                r"-l (meta.AccuracyUpdatedEnsemble -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01))",

                r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingTree -g 100 -c 0.01))",
                r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01))",

                r"-l (meta.OzaBoost -l trees.HoeffdingTree)"
                ]


  report0 =    [

                # Plain Hoeffding Tree

                r"-l trees.HoeffdingTree",

                # Show AUE2 doesn't outperform OzaBoost once you match grace and split decision values

                r"-l (meta.OzaBoost -l (trees.HoeffdingTree -g 100 -c 0.01))",
                r"-l (meta.OzaBoost -l (trees.HoeffdingTree))",
                r"-l meta.OnlineAccuracyUpdatedEnsemble",

                # HAT-ADWIN base, normal default values

                r"-l (meta.OzaBoost -l (trees.HATADWIN))",
                r"-l (meta.OnlineAccuracyUpdatedEnsemble -l (trees.HATADWIN))",

                # Is this required?
                #r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingTree -g 100 -c 0.01))",

                # Show how well HATADWIN does
                #r"-l (trees.HATADWIN) -g 100 -c 0.01)",
                r"-l (trees.HATADWIN)",
                r"-l (meta.OzaBoost -l (trees.HATADWIN -g 100 -c 0.1)) ",
                r"-l (meta.AccuracyUpdatedEnsemble -l (trees.HATADWIN -g 100 -c 0.01))",

                # Show OzaBoost is no beaten when wrapped with a change detector
                r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINMonotoneChangeDetector)",
                r"-l (drift.SingleClassifierDrift -l meta.OzaBoost -d ADWINMonotoneChangeDetector)",
                r"-l (drift.SingleClassifierDrift -l meta.AdaptableDiversityBasedOnlineBoosting -d ADWINMonotoneChangeDetector)",
                r"-l (drift.SingleClassifierDrift -l meta.BOLE -d ADWINMonotoneChangeDetector)",

                #r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01))",

                ]

  temp_1 = [
 #               r"-l (meta.OzaBoost -l (trees.HATADWIN -g 100 -c 0.1)) ",
                r"-l (meta.OzaBoost -l (trees.HATADWIN))",
#                r"-l trees.HATADWIN ",
          ]

  amnesia = [
                #r"-l trees.HoeffdingTree",
                #r"-l trees.VFDT",

                r"-l (trees.VFDTWindow -W 25000)",
                #r"-l (trees.VFDTWindow -W 50000)",
                r"-l (trees.VFDTWindow -W 75000)",
                r"-l (trees.VFDTWindow -W 125000)",
                #r"-l (trees.VFDTWindow -W 150000)",
                #r"-l (trees.VFDTWindow -W 200000)",

                r"-l (trees.VFDTLeafWindow -W 1000)",
                r"-l (trees.VFDTLeafWindow -W 5000)",
                r"-l (trees.VFDTLeafWindow -W 10000)",
                r"-l (trees.VFDTLeafWindow -W 12000)",
                r"-l (trees.VFDTLeafWindow -W 13000)",
                r"-l (trees.VFDTLeafWindow -W 15000)",

                #r"-l (trees.VFDTLeafWindowADWIN -W 25000)",
                #r"-l (trees.VFDTLeafWindowADWIN -W 50000)",
                #r"-l (trees.VFDTLeafWindowADWIN -W 75000)",
                #r"-l (trees.VFDTLeafWindowADWIN -W 125000)",

                #r"-l (trees.VFDTDecay -D 0.9999)",
          ]
 
  #learners = report0
  #learners = amnesia
  learners = learners_1

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

    gen_strings_gradual = [
            #r"ConceptDriftStream -s (generators.monash.AbruptDriftGenerator -o 0.800001 -c -n 4 -v 4 -r 1 -b 999999) -d (generators.monash.AbruptDriftGenerator -o 0.800001 -c -n 4 -v 4 -r 1 -b 1) -p 200000"
            #r"ConceptDriftStream -s (generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.700002 -c -n 4 -v 4 -r 1 -b 1) -p 200000 -w 2000 -r 1"
            r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.8 -c -n 4 -v 4 -r 1 -b 1) -w 4000",
            r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.5 -c -n 4 -v 4 -r 1 -b 1) -w 4000",
            r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.3 -c -n 4 -v 4 -r 1 -b 1) -w 4000",
            r"RecurrentConceptDriftStream -x 20000 -y 20000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.1 -c -n 4 -v 4 -r 1 -b 1) -w 4000"
            ]

    gen_strings_square_wave = [
            r"RecurrentConceptDriftStream -x 40000 -y 40000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.8 -c -n 4 -v 4 -r 1 -b 40001) -w 1",
            r"RecurrentConceptDriftStream -x 40000 -y 40000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.5 -c -n 4 -v 4 -r 1 -b 40001) -w 1",
            r"RecurrentConceptDriftStream -x 40000 -y 40000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.3 -c -n 4 -v 4 -r 1 -b 40001) -w 1",
            r"RecurrentConceptDriftStream -x 40000 -y 40000 -z 99 -s (generators.monash.AbruptDriftGenerator -n 4 -v 4 -r 1 -b 9999999) -d (generators.monash.AbruptDriftGenerator -o 0.1 -c -n 4 -v 4 -r 1 -b 40001) -w 1"
        ]


    gen_strings_exp_2_2 = [
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -r 1 -b 9999999 -o 0.0",
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -r 1 -b 100000 -o 0.3",
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -r 1 -b 100000 -o 0.5",
            r"generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -r 1 -b 100000 -o 0.8"
        ]

    gen_strings_exp_3_3 = [
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -r 1 -b 999999 -o 0.0",
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -r 1 -b 100000 -o 0.3",
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -r 1 -b 100000 -o 0.5",
            r"generators.monash.AbruptDriftGenerator -c -n 3 -v 3 -r 1 -b 100000 -o 0.8"
        ]

    gen_strings_exp_4_4 = [
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 9999999 -o 0.0",
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 150000 -o 0.3",
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 150000 -o 0.5",
            r"generators.monash.AbruptDriftGenerator -c -n 4 -v 4 -r 1 -b 150000 -o 0.8"
        ]

    gen_strings_gradual = [
            #r"ConceptDriftStream -p 200000 -w 100000 -s (generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 1 -b 99999999 -o 0.8) -d (generators.monash.AbruptDriftGenerator -c -n 2 -v 2 -z 2 -r 1 -b 1 -o 0.8)"
            r"ConceptDriftStream -p 200000 -w 100000 -s (generators.monash.AbruptDriftGenerator -c -z 2 -r 1 -b 99999999 -o 0.8) -d (generators.monash.AbruptDriftGenerator -c -z 2 -r 1 -b 1 -o 0.8)"
        ]

#EvaluatePrequential -l trees.HATADWIN -s (ConceptDriftStream -s (generators.RandomTreeGenerator -r 2 -i 2 -u 0) -d (generators.RandomTreeGenerator -r 3 -i 3 -u 0) -p 200000 -w 10 -r 20) -i 400000 -f 1000
    #gen_strings = gen_strings_abrupt_conditional
    #gen_strings = gen_strings_exp_1_4
    #gen_strings = gen_strings_square_wave
    #gen_strings = gen_strings_MOA_TREE
    gen_strings = gen_strings_exp_4_4

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

      # Add this folder's mean error column to the error_df 
      #error_df[str(folder)] = all_stream_mean_df['error'] 
      cpu_time = all_stream_mean_df['evaluation time (cpu seconds)'].iloc[int_evl_num_rows-1] 
      #print("+++++++++++" + str(jkl))
      error_df[str(folder)+ ' : ' + str(cpu_time) + 's'] = all_stream_mean_df['error']
      #error_df[str(folder)+" "+"5"] = all_stream_mean_df['error']

      mean_dataframes.append(all_stream_mean_df)

    # Set the index column
    # error_df[mcv.INDEX_COL]
    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    error_df = error_df.set_index(mcv.INDEX_COL)
    error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

    # Plot.plot_df(all_stream_mean_df)
    Plot.plot_df(error_df, exp.getCmd(), mcv.FIG_DIR+"/"+str(figNo))

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
        generator = gen.GeneratorBuilder.MonashAbruptDriftGenBuilder(nAttributes=4, nValuesPerAttribute=4, burnIn=100000, driftMagConditional=drift_mag, driftConditional=True, randomSeed=i+1)
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


