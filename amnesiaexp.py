
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
from multiprocessing import Process, Queue

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

    new_col_names = ["0:VFDT", "1:EideticVFDT"]
    for col in error_df.columns:
        new_col_names[int(col)] = (new_col_names[int(col)] + " | T:" + ("%.2f s"%runtime_dict[col]) + " | E: " + ("%.4f"%error_df[col].mean()))
    error_df.columns = new_col_names

    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(suffix).zfill(3), split_df)


def runMultiStreamExpML(title, learners, generators, evaluators, suffix, num_streams=1):
    # This one does Multiple Learners and a Single Generator on one plot

    new_col_names = ["VFDT", "EideticVFDT"]
    all_processes=[]
    # get 10 stream average for each learner
    gen_no = 0
    lrn_no = 0

    exp_dir = mcv.OUTPUT_DIR + "/" + str(suffix) # folder for this experiment
    output_dirs = []
    
    for learner in learners:
        lrn_no += 1
        lrn_dir = exp_dir + '/' + str(lrn_no)

        for gen_string in generators:
            gen_no += 1
            seeded_generators = []
            output_dir = lrn_dir+ "/" + str(gen_no)
            output_dirs.append(output_dir)
    
            # num_streams streams per generator
            for randomSeed in range(0, num_streams):
                gen_cmd = se.CompositeExperiment.multiSeededGenBuilder(gen_string, randomSeed)
                seeded_generators.append(gen_cmd)
    
            seeded_experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, [learner], seeded_generators)
    
            for exp in seeded_experiments:
                print(exp.cmd)
    
    #===================Comment these to just generate plots
            processes = se.CompositeExperiment.make_running_processes(seeded_experiments, output_dir)
            all_processes.extend(processes)
    
    exit_codes = [p.wait() for p in all_processes]
    #==================== 
    
        # List of mean dataframes
    mean_dataframes = []
        # Dataframe that contains all the mean error columns for the experiments
    error_df = pd.DataFrame([])
        # Dataframe that contains all the mean split columns for the experiments
    split_df = pd.DataFrame([])
    
        # average the streams, then plot
    for folder in output_dirs:
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

        error_df["Learner: " + new_col_names[int(os.path.basename(os.path.normpath(folder)))-1] + " | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.4f"%average_error) + ' |'] = all_stream_mean_df['error']
        split_df["Splits: " + new_col_names[int(os.path.basename(os.path.normpath(folder)))-1] + " "] = all_stream_mean_df['splits']

        mean_dataframes.append(all_stream_mean_df)

    # Set the index column
    # error_df[mcv.INDEX_COL]
    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]/1000 #MAGIC
    error_df = error_df.set_index(mcv.INDEX_COL)
    #error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

    split_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]/1000 #MAGIC
    split_df = split_df.set_index(mcv.INDEX_COL)
    #split_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Split.csv")

    #se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(23).zfill(3), split_df)
    se.Plot.plot_df(title, error_df, "Error", mcv.FIG_DIR+"/"+str(suffix).zfill(3), split_df)







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
    utilities.remove_folder(exp_dir)
    if not os.path.exists(exp_dir):
      os.makedirs(exp_dir)
####+++++++++++++++++

    lrn_ctr = -1
    output_dirs = []
    for learner in learners:
      lrn_ctr += 1
      singleLearnerList = []
      singleLearnerList.append(learner)
      output_dir = exp_dir + "/" + str(lrn_ctr) 
      output_dirs.append(output_dir)

#+++++++++++++++++ Comment this out in order to just draw charts without running experiments
      seeded_experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, singleLearnerList, seeded_generators)
      processes = se.CompositeExperiment.make_running_processes(seeded_experiments, output_dir)
      all_processes.extend(processes)

      exit_codes = [p.wait() for p in all_processes] # USE THIS ONE FOR FONTS so it doesn't overload RAM. 4Gig per process.
###+++++++++++++++++
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
    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(exp_no).zfill(3), split_df)
    #se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(exp_no).zfill(3), None)


def chart0():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
    r"-s (RecurrentConceptDriftStream -x 10000 -y 10000 -z 175 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 99999999) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 1 -b 1))"
            ]
    evaluators = [r"EvaluatePrequential -i 4000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 0)

 
def chart1():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
    #r"-s (RecurrentConceptDriftStream -x 100000 -y 100000 -z 75 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 99999999) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 1 -b 1))"
    r"-s (RecurrentConceptDriftStream -x 100000 -y 100000 -z 75 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 99999999) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 1 -b 9999999))"
            ]
    evaluators = [r"EvaluatePrequential -i 2000000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 1)
    runMultiStreamExpML(learners, generators, evaluators, str(1))

 
def chart2():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
    r"-s (RecurrentConceptDriftStream -x 200000 -y 200000 -z 175 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 99999999) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 1 -b 1))"
            ]
    evaluators = [r"EvaluatePrequential -i 4000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 2)


def chart3():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
    r"-s (RecurrentConceptDriftStream -x 100000 -y 100000 -z 175 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 50000) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 2 -b 50000))"
            ]
    evaluators = [r"EvaluatePrequential -i 200000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML(learners, generators, evaluators, str(3))

def chart4():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
    r"-s (RecurrentConceptDriftStream -x 100000 -y 100000 -z 175 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 50000) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 2 -b 50000))"
            ]
    evaluators = [r"EvaluatePrequential -i 600000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML(learners, generators, evaluators, str(4))

 
def chart5():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
    r"-s (RecurrentConceptDriftStream -x 200000 -y 200000 -z 175 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 99999999) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 1 -b 1))"
            ]
    evaluators = [r"EvaluatePrequential -i 1000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 5)


def chart6():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
    r"-s (RecurrentConceptDriftStream -x 100000 -y 100000 -z 1750 -w 1 -s (generators.monash.AbruptDriftGenerator -z 3 -n 3 -v 3 -r 1 -b 99999999) -d (generators.monash.AbruptDriftGenerator -c -z 3 -n 3 -v 3 -r 2 -b 9999999))"
            ]
    evaluators = [r"EvaluatePrequential -i 600000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML(learners, generators, evaluators, str(6))

#########################################

def chart7():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.HATADWIN"]
    generators= [
    r"-s (generators.monash.AbruptDriftGenerator -c  -o 0.7 -z 2 -n 2 -v 2 -r 2 -b 150000)"
            ]
    evaluators = [r"EvaluatePrequential -i 400000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML(learners, generators, evaluators, str(7))

def chart8():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.HATADWIN"]
    generators= [
    r"-s (generators.monash.AbruptDriftGenerator -c  -o 0.7 -z 3 -n 3 -v 3 -r 2 -b 150000)"
            ]
    evaluators = [r"EvaluatePrequential -i 400000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML(learners, generators, evaluators, str(8))


def chart9():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.HATADWIN"]
    generators= [
    r"-s (generators.monash.AbruptDriftGenerator -c  -o 0.7 -z 4 -n 4 -v 4 -r 2 -b 150000)"
            ]
    evaluators = [r"EvaluatePrequential -i 400000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML(learners, generators, evaluators, str(9))


def chart9():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.HATADWIN"]
    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 0.7 -z 5 -n 5 -v 5 -r 2 -b 150000)"
            ]
    evaluators = [r"EvaluatePrequential -i 400000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML(learners, generators, evaluators, str(9))


#########################################



def chart11():

    learners = [ r"-l trees.VFDT", 
            r"-l trees.VFDTUnforgetting"]
    generators= [
        r"-s (generators.monash.AbruptDriftGenerator -c  -o 0.7 -z 5 -n 5 -v 5 -r 2 -b 150000)"
            ]
    evaluators = [r"EvaluatePrequential -i 400000 -f 1000 -q 1000"]
    #runexp(learners, generators, evaluators, 3)
    runMultiStreamExpML("VFDT vs Eidetic VFDT: Abrupt Drift", learners, generators, evaluators, str(11))








    # without the main sentinel below code will always get run, even when imported as a module!
if __name__=="__main__": 

    processes = {}
#
#    processes[0] = Process(target=chart0)  #Recurrent Drift
#    processes[1] = Process(target=chart1)  #Recurrent Drift
#    processes[2] = Process(target=chart2)  #Recurrent Drift
#    processes[3] = Process(target=chart3)  #Recurrent Drift
#    processes[4] = Process(target=chart4)  #Recurrent Drift
#    processes[5] = Process(target=chart5)  #Recurrent Drift
#    processes[6] = Process(target=chart6)  #Recurrent Drift
##    processes[7] = Process(target=chart7)  #Recurrent Drift
#    processes[8] = Process(target=chart8) # Recurrent Drift
#    processes[9] = Process(target=chart9) # Recurrent Drift
##    processes[24] = Process(target=chart24) # Synthetic EFDT nominal
    processes[11] = Process(target=chart11) 

    #processes[28] = Process(target=chart28)  # Chess

    for key in processes:
      processes[key].start()
  

