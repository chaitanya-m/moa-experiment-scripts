
import os
import sys
import utilities
import re
import math
import subprocess
import shlex
import string
import pandas as pd
import simpleExperiments as se
import moa_command_vars as mcv
import time
from multiprocessing import Process, Queue

num_streams_to_average = 10
random_source_str = r'--random-source=<( openssl enc -aes-256-ctr -pass pass:seed -nosalt </dev/zero 2>/dev/null)'

def runexp(learners, generators, evaluators, suffix):
    output_dir = mcv.OUTPUT_DIR + "/" + str(suffix)
    experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, learners, generators)
#---------- Comment these lines out to get just charts
    processes = se.CompositeExperiment.make_running_processes(experiments, output_dir)
    se.Utils.wait_for_processes(processes)
#----------

    error_df = se.Utils.error_df_from_folder(output_dir)
    runtime_dict = se.Utils.runtime_dict_from_folder(output_dir)
    split_df = se.Utils.split_df_from_folder(output_dir)
    end_stats_from_folder_dict = se.Utils.end_stats_from_folder(output_dir)

    new_col_names = learners #["0:VFDT", "1:EideticVFDT"]
    for col in error_df.columns:
        new_col_names[int(col)] = (new_col_names[int(col)] + " | T:" + ("%.2f s"%runtime_dict[col]) + " | E: " + ("%.4f"%error_df[col].mean()))
    error_df.columns = new_col_names

    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(suffix).zfill(3), split_df, end_stats_from_folder_dict)

def getOutputDir(exp_dir, learner, generator):

    lrn_dir = exp_dir + '/' + learner
    output_dir = lrn_dir + '/' + generator
    return output_dir

def runMultiStreamExpML(title, learners, generators, evaluators, expDirName, num_streams=num_streams_to_average, numparallel=20):
    # This one does Multiple Learners and Generators

    running_processes = []

    exp_dir = mcv.OUTPUT_DIR + "/" + str(expDirName) # folder for this experiment

    new_col_names_counter = 0
       
    for learner in learners:
        for gen_string in generators:
            output_dir = getOutputDir(exp_dir, learner, gen_string)
            seeded_generators = []
            for randomSeed in range(0, num_streams): # num_streams streams to average per generator
                gen_cmd = se.CompositeExperiment.multiSeededGenBuilder(gen_string, randomSeed)
                seeded_generators.append(gen_cmd)
    
            seeded_experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, [learner], seeded_generators)
    
            for exp in seeded_experiments:
                print(exp.cmd)
    
            processes = se.CompositeExperiment.make_running_processes(seeded_experiments, output_dir)
            running_processes.extend(processes)

            if len(running_processes) > numparallel:
                exit_codes = [p.wait() for p in running_processes]
                running_processes = []
    
def makeChart(title, learners, generators, evaluators, expDirName, num_streams=num_streams_to_average):

    exp_dir = mcv.OUTPUT_DIR + "/" + str(expDirName) # folder for this experiment

    table = {}
    cells = {}
    output_dirs = []
    for learner in learners:
        table[learner] = {} # table has learners as keys
        for gen_string in generators:
            output_dir = getOutputDir(exp_dir, learner, gen_string)
            output_dirs.append(output_dir)
            # table[learner] has generators as keys. Values are cells, each should be a dict with Accuracy, Time, etc as fields
            # then, we need to map output_dirs to the cells so we know where to put our results.
            table[learner][gen_string] = {}
            cells[output_dir] = table[learner][gen_string]
 
        # List of mean dataframes
    mean_dataframes = []
        # Dataframe that contains all the mean error columns for the experiments
    error_df = pd.DataFrame([])
        # Dataframe that contains all the mean split columns for the experiments
    split_df = pd.DataFrame([])
    
        # create dictionaries for other variables
    fieldTokens = mcv.FIELDS.split(',')
    fieldTokensAvg = mcv.FIELDS_AVG.split(',')
    dict_of_dicts = {}
    dict_of_dicts_avg = {}
    for field in fieldTokens:
        dict_of_dicts[field] = dict()
    for field in fieldTokensAvg:
        dict_of_dicts_avg[field] = dict()

        # average the streams, then plot

    for folder in output_dirs:
        files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        dataframes = []
        for this_file in files:
            #print(this_file)
            #dataframes.append(pd.read_csv(this_file))
            dataframes.append(pd.read_csv(this_file, index_col=False, header=0, skiprows=0))

        all_stream_learning_data = pd.concat(dataframes)
        all_stream_mean = {}
        num_rows = dataframes[0].shape[0]

        for i in range(num_rows):
            all_stream_mean[i] = all_stream_learning_data[i::num_rows].mean()

        all_stream_mean_df = pd.DataFrame(all_stream_mean).transpose()
        all_stream_mean_df['error'] = (100.0 - all_stream_mean_df['classifications correct (percent)'])/100.0

        average_error = all_stream_mean_df['error'].sum()/num_rows
        cpu_time = all_stream_mean_df['evaluation time (cpu seconds)'].iloc[num_rows-1] # yes this is avg cpu_time
        cells[folder]["E"] = average_error
        cells[folder]["T"] = cpu_time

        error_df[folder.replace(exp_dir,'')
                + " | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.4f"%average_error) + ' |'] = all_stream_mean_df['error']
        mean_dataframes.append(all_stream_mean_df)

        for field in dict_of_dicts.keys():
            dict_of_dicts[field][folder.replace(exp_dir,'')] = all_stream_mean_df[field].iloc[-1]
        for field in dict_of_dicts_avg.keys():
            dict_of_dicts_avg[field][folder.replace(exp_dir,'')] = all_stream_mean_df[field].sum()/num_rows

      # Only mark actual splits as 1 and discard the rest of the split counts
# splits are only available for some learners.
#        splitArray = all_stream_mean_df['splits']
#        i = 0
#        while i < splitArray.size-1:
#      #print(str(i+1) + " " + str(splitArray[i+1]) + "\n")
#            diff = math.floor(splitArray[i+1]) - math.floor(splitArray[i])
#            if(diff > 0):
#                splitArray[i+1] = (-1)*diff
#                i = i+2
#            else:
#                i=i+1
#        for i in range(splitArray.size):
#            if(splitArray[i] > 0):
#                splitArray[i] = 0
#            else:
#                splitArray[i] = (-1) * splitArray[i]
#
# splits are only available for some learners        
#        split_df["Splits: " + folder.replace(exp_dir,'')
#                #new_col_names[int(os.path.basename(os.path.normpath(folder)))-1] 
#                #new_col_names[col_name_counter] # Use for papers, pass new_col_names
#                + " "] = all_stream_mean_df['splits']
#

    print(table)
    print(cells)
    df_table = pd.concat({k: pd.DataFrame(v) for k, v in table.items()})
    df_table.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Table.csv")

    # Set the index column
    # error_df[mcv.INDEX_COL]

    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]/1000 #MAGIC
    error_df = error_df.set_index(mcv.INDEX_COL)

    #error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

# splits are only available for some learners        
#    split_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]/1000 #MAGIC
#    split_df = split_df.set_index(mcv.INDEX_COL)
    #split_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Split.csv")

    #se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(23).zfill(3), split_df)
    #se.Plot.plot_df(title, error_df, "Error", mcv.FIG_DIR+"/"+str(expDirName).zfill(3), split_df)

    #df_end = pd.concat({k: pd.DataFrame.from_dict(v, 'index') for k, v in dict_of_dicts.items()}, axis=0)

    df_end = pd.DataFrame(dict_of_dicts).T # get dataframe with final values
    df_avg = pd.DataFrame(dict_of_dicts_avg).T # get dataframe with final values
    #se.Plot.plot_df(title, error_df, "Error", mcv.FIG_DIR+"/"+str(expDirName).zfill(3), None, df_end, df_avg) # no splits

    #se.Plot.plot_df(title, error_df, "Error", mcv.FIG_DIR+"/"+str(expDirName).zfill(3), split_df, df_end, df_avg)



def shuffledRealExpOps(exp_no, num_streams, learners, generator_template, evaluators, shuf_prefix, head_prefix, tail_prefix):

    subprocesses= []
    files = []
    seeded_generators=[]

#================== Run without this in order to not have to redo all the shuffling
    # Generate the shuffled tails for the streams
    for i in range(0, num_streams):

      subprocesses.append(subprocess.Popen(['shuf -o ' + shuf_prefix + str(i) + ' ' + tail_prefix + ' '
	+ string.replace(random_source_str, 'seed', str(i)) ], shell=True, executable = '/bin/bash'))
    # Need executable = /bin/bash, Otherwise it will use /bin/sh, which on Ubuntu is dash, a basic shell that doesn't recognize ( symbols

    exit_codes = [p.wait() for p in subprocesses] # Wait- Ensure all shuffled tails have been created    
    subprocesses = []

#==================

    # Generate the final arffs through concatenation with heads, and the respective generators
    for i in range(0, num_streams):
      files.append(' ' + shuf_prefix + str(i) + '.arff')
      seeded_generators.append(re.sub('(\/.*)+\.arff', files[i], generator_template))


#================== Run without this in order to not have to redo all the shuffling
      print(re.sub('(\/.*)+\.arff', files[i], generator_template))
      subprocesses.append(subprocess.Popen(['cat ' + ' ' + head_prefix + ' ' + 
	' ' + shuf_prefix + str(i) +'>'+ str(files[i])], shell=True, executable = '/bin/bash'))
    exit_codes = [p.wait() for p in subprocesses]
    subprocesses = []
#==================


    # Now run experiments for each learner on all the arffs
    all_processes=[]
    exp_dir = mcv.OUTPUT_DIR + "/" + str(exp_no) 

    os.chdir(mcv.MOA_DIR)
#+++++++++++++++++ Comment this out in order to just draw charts without running experiments
#    utilities.remove_folder(exp_dir)
#    if not os.path.exists(exp_dir):
#      os.makedirs(exp_dir)
#####+++++++++++++++++

    lrn_ctr = -1
    output_dirs = []
    for learner in learners:
      lrn_ctr += 1
      singleLearnerList = []
      singleLearnerList.append(learner)
      output_dir = exp_dir + "/" + str(lrn_ctr) 
      output_dirs.append(output_dir)

#+++++++++++++++++ Comment this out in order to just draw charts without running experiments
#      seeded_experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, singleLearnerList, seeded_generators)
#      processes = se.CompositeExperiment.make_running_processes(seeded_experiments, output_dir)
#      all_processes.extend(processes)
#
#      exit_codes = [p.wait() for p in all_processes] # USE THIS ONE FOR FONTS so it doesn't overload RAM. 4Gig per process.
####+++++++++++++++++
    #exit_codes = [p.wait() for p in all_processes]
 


    # List of mean_dataframes
    mean_dataframes = []
    # Dataframe that contains all the mean error columns for the experiments
    error_df = pd.DataFrame([])
    # Dataframe that contains all the mean split columns for the experiments
    split_df = pd.DataFrame([])

    folder_ctr = -1
    # average the streams, then plot
    for folder in output_dirs:
      folder_ctr+=1
      files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
      dataframes = []
      for this_file in files:
        dataframes.append(pd.read_csv(this_file, index_col=False, header=0, skiprows=0))

      all_stream_learning_data = pd.concat(dataframes)
      all_stream_mean = {}
      num_rows = dataframes[0].shape[0] 
      for i in range(num_rows):
        all_stream_mean[i] = all_stream_learning_data[i::num_rows].mean()
      all_stream_mean_df = pd.DataFrame(all_stream_mean).transpose()
    #runexp23(learners, generators, evaluators, 23)
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

      # Add this folder's mean error column to the error_df 
      #error_df[str(folder)] = all_stream_mean_df['error'] 
      average_error = all_stream_mean_df['error'].sum()/num_rows
      cpu_time = all_stream_mean_df['evaluation time (cpu seconds)'].iloc[num_rows-1] # yes this is avg cpu_time
      #print("+++++++++++" + str(jkl))
      #error_df[" M: "+ str(folder)+ " | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      legend_str = ''
      if folder_ctr == 0:
        legend_str = 'VFDT'
      else:
	legend_str = 'EFDT'

      error_df[legend_str + ": | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.4f"%average_error) + ' |'] = all_stream_mean_df['error']
      #error_df["Classes : "  + os.path.basename(os.path.normpath(folder))+ " | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      #error_df[" | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      #error_df[str(folder)+" "+"5"] = all_stream_mean_df['error']
      #split_df["splits " + os.path.basename(os.path.normpath(folder))] = all_stream_mean_df['splits']
      split_df["Splits: " + legend_str] = all_stream_mean_df['splits']

      mean_dataframes.append(all_stream_mean_df)

    # Set the index column
    # error_df[mcv.INDEX_COL]
    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]/1000 # MAGIC NUMBER!!- its the measurement frequency
    error_df = error_df.set_index(mcv.INDEX_COL)
    #error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

    split_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]/1000 # MAGIC NUMBER!!
    split_df = split_df.set_index(mcv.INDEX_COL)
    #split_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Split.csv")

    #se.Plot.plot_df(error_df, " ", mcv.FIG_DIR+"/"+str(figNo).zfill(3), split_df)
#    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(exp_no).zfill(3), split_df)
    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(exp_no).zfill(3), None)


#########################################

def chart4():

    learners = [ 
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            r"-l (meta.LeveragingBag -l trees.EFDT -a 1.0)"
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)"
            ]
    evaluators = [r"EvaluatePrequential -i 5000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Leveraging Bagging: EFDT (ADWIN disabled) vs VFDT", learners, generators, evaluators, str('4'))

def chart5():

    learners = [ 
            r"-l (meta.OzaBoost -l trees.VFDT)",
            r"-l (meta.OzaBoost -l trees.EFDT)"
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)"
            ]
    evaluators = [r"EvaluatePrequential -i 5000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("OzaBoost: EFDT vs VFDT", learners, generators, evaluators, str('5'))

def chart6():

    learners = [ 
            r"-l trees.EFDTBoost",
            r"-l trees.HATErrorRedist"
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)"
            ]
    evaluators = [r"EvaluatePrequential -i 5000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("EFDTBoost vs HATErrorRedist", learners, generators, evaluators, str('6'))


def chart7():

    learners = [ 
            r"-l trees.HATADWIN",
            r"-l trees.HATErrorRedist"
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)"
            ]
    evaluators = [r"EvaluatePrequential -i 5000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("HAT vs HATErrorRedist", learners, generators, evaluators, str('7'))

def chart8():

    learners = [ 
            r"-l trees.HATADWIN",
            r"-l trees.EFDT"
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)"
            ]
    evaluators = [r"EvaluatePrequential -i 5000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("HAT vs EFDT", learners, generators, evaluators, str('8'))


def chart9():

    learners = [ 
            r"-l trees.HATADWIN",
            r"-l trees.HATErrorRedist"
            r"-l trees.EFDTBoost",
            r"-l trees.EFDT",
            r"-l trees.VFDT",
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("HAT", learners, generators, evaluators, str('9'))



def chart10():

    learners = [ 
            r"-l trees.HATADWIN",
            ] 

    generators= [
        r"-s (generators.RandomRBFGeneratorDrift -s 0.001 -k 50)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.001 -k 10)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.0001 -k 50)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.0001 -k 10)",
           ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("HAT", learners, generators, evaluators, str('10'),1)



def chart11():

    learners = [ 
            r"-l trees.HATADWIN",
            ] 

    generators= [
        r"-s (generators.HyperplaneGenerator -k 10 -t 0.001)",
        r"-s (generators.HyperplaneGenerator -k 10 -t 0.0001)",
        r"-s (generators.SEAGenerator -n 50)",
        r"-s (generators.SEAGenerator -n 50000)",
        r"-s (ArffFileStream -f /mnt/datasets/covtype/covtypeNorm.arff)"
           ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("HAT", learners, generators, evaluators, str('11'),1)


def chart12():

    learners = [ 
            r"-l trees.HATADWIN",
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            r"-l (meta.OzaBag -l trees.VFDT)",
            r"-l (meta.OzaBagAdwin -l trees.VFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.VFDT)",
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("HAT and some ensembles", learners, generators, evaluators, str('12'))




def chart13():

    learners = [ 
            r"-l trees.HATADWIN",
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            r"-l (meta.OzaBag -l trees.VFDT)",
            r"-l (meta.OzaBagAdwin -l trees.VFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.VFDT)",
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
          ]
    evaluators = [r"EvaluatePrequential -i 5000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("HAT and some ensembles", learners, generators, evaluators, str('13'))







def chart14():

    learners = [ 
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            ] 

    generators= [
        r"-s (generators.RandomRBFGeneratorDrift -s 0.001 -k 50)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.001 -k 10)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.0001 -k 50)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.0001 -k 10)",
           ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Leveraging Bagging VFDT", learners, generators, evaluators, str('14'),1)



def chart15():

    learners = [ 
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            ] 

    generators= [
        r"-s (generators.HyperplaneGenerator -k 10 -t 0.001)",
        r"-s (generators.HyperplaneGenerator -k 10 -t 0.0001)",
        r"-s (generators.SEAGenerator -n 50)",
        r"-s (generators.SEAGenerator -n 50000)",
        r"-s (ArffFileStream -f /mnt/datasets/covtype/covtypeNorm.arff)"
           ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Leveraging Bagging VFDT", learners, generators, evaluators, str('15'),1)



def chart16():

    learners = [ 
            r"-l trees.VFDT",
            r"-l trees.RandomVFDT",
            r"-l (trees.VFDTDecay -D 0.1)",
            r"-l (trees.VFDTDecay -D 0.9)",
            r"-l trees.EFDT",
            r"-l trees.EFDTBoost",
            r"-l trees.HATADWIN",
            r"-l trees.HATErrorRedist",
            r"-l trees.CVFDT",
            r"-l trees.DecisionStump",
           ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('16'), 10)



def chart17():

    learners = [ 
            r"-l (meta.OzaBag -l trees.VFDT)",
            r"-l (meta.OzaBagAdwin -l trees.VFDT)",
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.VFDT)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.VFDT)",
            r"-l (meta.BOLE -l trees.VFDT)",
            r"-l (meta.OnlineSmoothBoost -l trees.VFDT)",
            #r"-l (meta.OzaBagASHT -l trees.VFDT)",
            #r"-l (meta.OnlineAccuracyUpdatedEnsemble -l trees.VFDT)",
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('17'), 10)


def chart18():

    learners = [ 
            r"-l (meta.OzaBag -l trees.EFDT)",
            r"-l (meta.OzaBagAdwin -l trees.EFDT)",
            r"-l (meta.LeveragingBag -l trees.EFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.EFDT)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.EFDT)",
            r"-l (meta.BOLE -l trees.EFDT)",
            r"-l (meta.OnlineSmoothBoost -l trees.EFDT)",
            #r"-l (meta.OzaBagASHT -l trees.EFDT)",
            #r"-l (meta.OnlineAccuracyUpdatedEnsemble -l trees.EFDT)",
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('18'), 10)


def chart19():

    learners = [ 
            r"-l (meta.OzaBag -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OzaBagAdwin -l trees.DecisionStumpBugfixed)",
            r"-l (meta.LeveragingBag -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OzaBoostAdwin -l trees.DecisionStumpBugfixed)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.DecisionStumpBugfixed)",
            r"-l (meta.BOLE -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OnlineSmoothBoost -l trees.DecisionStumpBugfixed)",
            #r"-l (meta.OzaBagASHT -l trees.DecisionStump)",
            #r"-l (meta.OnlineAccuracyUpdatedEnsemble -l trees.DecisionStump)",
            ] 

    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('19'), 10)



def chart20():

    learners = [ 
            r"-l (meta.OzaBag -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OzaBagAdwin -l trees.DecisionStumpBugfixed)",
            r"-l (meta.LeveragingBag -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OzaBoostAdwin -l trees.DecisionStumpBugfixed)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.DecisionStumpBugfixed)",
            r"-l (meta.BOLE -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OnlineSmoothBoost -l trees.DecisionStumpBugfixed)",
            #r"-l (meta.OzaBagASHT -l trees.DecisionStump)",
            #r"-l (meta.OnlineAccuracyUpdatedEnsemble -l trees.DecisionStump)",
            ] 

    generators= [
        r"-s (ArffFileStream -f /mnt/datasets/covtype/covtypeNorm.arff)"
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('20'), 10)



def chart21():

    learners = [
            r"-l (meta.OzaBag -l trees.VFDT)",
            r"-l (meta.OzaBagAdwin -l trees.VFDT)",
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.VFDT)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.VFDT)",
            r"-l (meta.BOLE -l trees.VFDT)",
            r"-l (meta.OnlineSmoothBoost -l trees.VFDT)",
            #r"-l (meta.OzaBagASHT -l trees.VFDT)",
            #r"-l (meta.OnlineAccuracyUpdatedEnsemble -l trees.VFDT)",
            ] 

    generators= [
        r"-s (ArffFileStream -f /mnt/datasets/covtype/covtypeNorm.arff)"
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('21'), 10)



def chart22():

    learners = [ 
            r"-l (meta.OzaBag -l trees.EFDT)",
            r"-l (meta.OzaBagAdwin -l trees.EFDT)",
            r"-l (meta.LeveragingBag -l trees.EFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.EFDT)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.EFDT)",
            r"-l (meta.BOLE -l trees.EFDT)",
            r"-l (meta.OnlineSmoothBoost -l trees.EFDT)",
            #r"-l (meta.OzaBagASHT -l trees.EFDT)",
            #r"-l (meta.OnlineAccuracyUpdatedEnsemble -l trees.EFDT)",
            ] 

    generators= [
        r"-s (ArffFileStream -f /mnt/datasets/covtype/covtypeNorm.arff)"
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('22'), 10)


def chart23():

    learners = [ 
            r"-l trees.VFDT",
            r"-l trees.RandomVFDT",
            r"-l (trees.VFDTDecay -D 0.1)",
            r"-l (trees.VFDTDecay -D 0.9)",
            r"-l trees.EFDT",
            r"-l trees.EFDTBoost",
            r"-l trees.HATADWIN",
            r"-l trees.HATErrorRedist",
            r"-l trees.CVFDT",
            r"-l trees.DecisionStump",
            ] 

    generators= [
        r"-s (ArffFileStream -f /mnt/datasets/covtype/covtypeNorm.arff)"
          ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('23'), 10)



def chart24():

    lmetaDecisionStump = [ 
            r"-l (meta.OzaBag -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OzaBagAdwin -l trees.DecisionStumpBugfixed)",
            r"-l (meta.LeveragingBag -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OzaBoostAdwin -l trees.DecisionStumpBugfixed)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.DecisionStumpBugfixed)",
            r"-l (meta.BOLE -l trees.DecisionStumpBugfixed)",
            r"-l (meta.OnlineSmoothBoost -l trees.DecisionStumpBugfixed)",
            ]
    lmetaEFDT = [ 
            r"-l (meta.OzaBag -l trees.EFDT)",
            r"-l (meta.OzaBagAdwin -l trees.EFDT)",
            r"-l (meta.LeveragingBag -l trees.EFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.EFDT)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.EFDT)",
            r"-l (meta.BOLE -l trees.EFDT)",
            r"-l (meta.OnlineSmoothBoost -l trees.EFDT)",
            r"-l (meta.ARF -l ARFEFDT)",
            ] 
    lmetaVFDT = [ 
            r"-l (meta.OzaBag -l trees.VFDT)",
            r"-l (meta.OzaBagAdwin -l trees.VFDT)",
            r"-l (meta.LeveragingBag -l trees.VFDT)",
            r"-l (meta.OzaBoostAdwin -l trees.VFDT)",
            r"-l (meta.AdaptableDiversityBasedOnlineBoosting -l trees.VFDT)",
            r"-l (meta.BOLE -l trees.VFDT)",
            r"-l (meta.OnlineSmoothBoost -l trees.VFDT)",
            r"-l (meta.ARF -l ARFVFDT)",
            ] 
    ltrees = [ 
            r"-l trees.VFDT",
            r"-l trees.RandomVFDT",
            r"-l (trees.VFDTDecay -D 0.1)",
            r"-l (trees.VFDTDecay -D 0.5)",
            r"-l (trees.VFDTDecay -D 0.9)",
            r"-l (trees.EFDTDecay -D 0.1)",
            r"-l (trees.EFDTDecay -D 0.5)",
            r"-l (trees.EFDTDecay -D 0.9)",
            r"-l trees.EFDT",
            r"-l trees.EFDTBoost",
            r"-l trees.HATADWIN",
            r"-l trees.HATErrorRedist",
            r"-l trees.CVFDT",
            r"-l trees.ECVFDT",
            r"-l trees.DecisionStumpBugfixed",
            ] 





    gsyntheticNoiseFree = [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 2 -n 2 -v 2 -r 2 -b 200000 -d Recurrent)",
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 2 -v 2 -r 2 -b 200000 -d Recurrent)",
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 4 -n 2 -v 2 -r 2 -b 200000 -d Recurrent)",
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 5 -n 2 -v 2 -r 2 -b 200000 -d Recurrent)",

        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 2 -r 2 -b 200000 -d Recurrent)",
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 3 -r 2 -b 200000 -d Recurrent)",
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 4 -r 2 -b 200000 -d Recurrent)",
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 3 -n 3 -v 5 -r 2 -b 200000 -d Recurrent)",


        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 4 -n 4 -v 4 -r 2 -b 200000 -d Recurrent)",
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 1.0 -z 5 -n 5 -v 5 -r 2 -b 200000 -d Recurrent)",
          ]


    gHyperplane = [
        r"-s (generators.HyperplaneGenerator -k 20 -t 0.01)",
        r"-s (generators.HyperplaneGenerator -k 20 -t 0.001)",
        r"-s (generators.HyperplaneGenerator -k 20 -t 0.0001)",
        r"-s (generators.HyperplaneGenerator -k 5 -t 0.01)",
        r"-s (generators.HyperplaneGenerator -k 5 -t 0.001)",
        r"-s (generators.HyperplaneGenerator -k 5 -t 0.0001)",
        ]
    gSEA = [
        r"-s (generators.SEAGenerator -n 50)",
        r"-s (generators.SEAGenerator -n 50000)",
        r"-s (generators.SEAGenerator -n 100000)",
        r"-s (generators.SEAGenerator -n 200000)",
        ]

    gRBF = [
        r"-s (generators.RandomRBFGeneratorDrift -s 0.001 -k 50)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.001 -k 10)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.0001 -k 50)",
        r"-s (generators.RandomRBFGeneratorDrift -s 0.0001 -k 10)",
           ]
 
    gReal= [
        r"-s (ArffFileStream -f /mnt/datasets/covtype/covtypeNorm.arff)",
        r"-s (ArffFileStream -f /mnt/datasets/cpe/cpe.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/sensor/sensor.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/airlineshuf.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/skin/skin.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/pamap2/pamap2_9subjects_unshuf.arff -c 2)",
        r"-s (ArffFileStream -f /mnt/datasets/fonts/fonts.arff -c 1)",
        r"-s (ArffFileStream -f /mnt/datasets/chess.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/wisdm/wisdm.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/kdd/KDDCup99_full.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/harpagwag/harpagwag.arff -c -1)",
        r"-s (ArffFileStream -f /mnt/datasets/poker/poker-lsn.arff -c -1)",

          ]

    learners = lmetaDecisionStump 
        + lmetaVFDT 
        + lmetaEFDT 
        + ltrees

    generators = gsyntheticNoiseFree
        + gHyperplane
        + gSEA
        + gRBF
        + gReal

    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("Diversity vs Adaptation", learners, generators, evaluators, str('24'), 10)
    #time.sleep(10)
    #makeChart("Diversity vs Adaptation", learners, generators, evaluators, str('24'), 10)



    # without the main sentinel below code will always get run, even when imported as a module!
if __name__=="__main__": 

    processes = {}



# Leveraging Bagging
#    processes[4] = Process(target=chart4)  #Recurrent Drift
#    processes[5] = Process(target=chart5)  #Recurrent Drift
#    processes[6] = Process(target=chart6)  #Recurrent Drift

#    processes[7] = Process(target=chart7)  #Recurrent Drift
#    processes[8] = Process(target=chart8)  #Recurrent Drift


#    processes[9] = Process(target=chart9)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[10] = Process(target=chart10)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[11] = Process(target=chart11)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[12] = Process(target=chart12)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[13] = Process(target=chart13)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[14] = Process(target=chart14)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[15] = Process(target=chart15)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[16] = Process(target=chart16)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[17] = Process(target=chart17)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[18] = Process(target=chart18)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[19] = Process(target=chart19)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[20] = Process(target=chart20)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[21] = Process(target=chart21)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[22] = Process(target=chart22)  #bunch of things with Drift from Bifet Leveraging Bagging paper
#    processes[23] = Process(target=chart23)  #bunch of things with Drift from Bifet Leveraging Bagging paper
    processes[24] = Process(target=chart24)  #bunch of things with Drift from Bifet Leveraging Bagging paper





    for key in processes:
      processes[key].start()
  

