
import os
import sys
import utilities
import re
import math
import pandas as pd
import simpleExperiments as se
import moa_command_vars as mcv
from multiprocessing import Process, Queue

def runexp(learners, generators, evaluators, suffix):
    output_dir = mcv.OUTPUT_DIR + "/" + str(suffix)
    experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, learners, generators)
    processes = se.CompositeExperiment.make_running_processes(experiments, output_dir)
    se.Utils.wait_for_processes(processes)

    error_df = se.Utils.error_df_from_folder(output_dir)
    runtime_dict = se.Utils.runtime_dict_from_folder(output_dir)
    split_df = se.Utils.split_df_from_folder(output_dir)

    new_col_names = ["VFDT", "EFDT"]
    for col in error_df.columns:
        new_col_names[int(col)] = (str(col)+ ": "+ new_col_names[int(col)] + " | T:" + ("%.2f s"%runtime_dict[col]) + " | E: " + ("%.6f"%error_df[col].mean()))
    error_df.columns = new_col_names

    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(suffix).zfill(3), split_df)

def runexp23(learners, generators, evaluators, suffix):
    output_dir = mcv.OUTPUT_DIR + "/" + str(suffix)
    experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, learners, generators)
    processes = se.CompositeExperiment.make_running_processes(experiments, output_dir)
    se.Utils.wait_for_processes(processes)

    error_df = se.Utils.error_df_from_folder(output_dir)
    runtime_dict = se.Utils.runtime_dict_from_folder(output_dir)
    split_df = se.Utils.split_df_from_folder(output_dir)

    new_col_names = ["VFDT2", "VFDT3", "VFDT4", "VFDT5"]#, "EFDT2", "EFDT3", "EFDT4", "EFDT5", ]
    for col in error_df.columns:
        new_col_names[int(col)] = (str(col)+ ": "+ new_col_names[int(col)] + " | T:" + ("%.2f s"%runtime_dict[col]) + " | E: " + ("%.6f"%error_df[col].mean()))
    error_df.columns = new_col_names

    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(suffix).zfill(3), split_df)

def chart1():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/hepmass.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]

    runexp(learners, generators, evaluators, 1)

def chart2():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/wisdmshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 2)

def chart3():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/susy.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 3)

def chart4():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/airlines.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 4)

def chart5():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/kddshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 5)

def chart6():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/higgsOrig.arff -c 33)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 6)

def chart7():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/poker-lsn.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 7)

def chart8():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/pokershuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 8)

def chart9():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/CovPokElec.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 9)

def chart10():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/cpeshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 10)

def chart11():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/covtypeNorm.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 11)

def chart12():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/covtypeshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 12)


def chart13():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/airlineshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 13)

def chart14():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3covtype.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 14)

def chart15():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3airlines.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 15)

def chart16():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3wisdm.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 16)

def chart17():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3kdd.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 17)

def chart18():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/skinshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 18)


def chart19():

    learners = [ r"-l trees.VFDT", r"-l (trees.EFDT -R 2000)"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/pamap2_9subjectsshuf.arff -c 2)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 19)

def chart20():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/fontshuf.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 20)

def chart21():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/chessshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 21)

def chart22():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/chessshufdiscrete.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 20000000 -f 1000 -q 1000"]
    runexp(learners, generators, evaluators, 22)

def chart23():

    learners = [ r"-l trees.VFDT" ]#, r"-l trees.EFDT"]
    generators = [
            r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 2 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
            r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 3 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
            r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 4 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
            r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 5 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",

    ]
    evaluators = [ r"EvaluatePrequential -i 400000 -f 1000 -q 1000" ]
    num_rows = int(400000/1000)


    all_processes = []
    # get 10 stream average for each generator
    gen_no = 1
    exp_dir = mcv.OUTPUT_DIR + "/" + str(23) 
    output_dirs = []
    for gen_string in generators:
      seeded_generators = []
      gen_no += 1
      output_dir = exp_dir + "/" + str(gen_no) 
      output_dirs.append(output_dir)

      for randomSeed in range(0, 10): #random seed for tree; generate 10 random streams  for this generator
        gen_cmd = re.sub("-r [0-9]+", "-r "+ str(randomSeed)+ " ", str(gen_string))
	#print(gen_cmd)
        seeded_generators.append(gen_cmd)

      seeded_experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, learners, seeded_generators)
      processes = se.CompositeExperiment.make_running_processes(seeded_experiments, output_dir)
      all_processes.extend(processes)

    exit_codes = [p.wait() for p in all_processes]
 
    # List of mean_dataframes
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
      error_df[" Classes: "+ os.path.basename(os.path.normpath(folder))+ " | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      #error_df[" | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      split_df["splits" + os.path.basename(os.path.normpath(folder))] = all_stream_mean_df['splits']
      #error_df[str(folder)+" "+"5"] = all_stream_mean_df['error']

      mean_dataframes.append(all_stream_mean_df)

    # Set the index column
    # error_df[mcv.INDEX_COL]
    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    error_df = error_df.set_index(mcv.INDEX_COL)
    #error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

    split_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    split_df = split_df.set_index(mcv.INDEX_COL)
    #split_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Split.csv")

    #se.Plot.plot_df(error_df, " ", mcv.FIG_DIR+"/"+str(figNo).zfill(3), split_df)
    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(23).zfill(3), split_df)


def chart24():

    learners = [ r"-l (trees.EFDT -c 0.2 -t 0.5)"]
    generators = [
            #r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 2 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
            #r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 3 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
            #r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 4 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",
            r"-s (generators.RandomTreeGenerator -r 1 -i 1 -c 5 -o 5 -u 0 -v 5 -d 5 -l 3 -f 0.15)",

    ]
    evaluators = [ r"EvaluatePrequential -i 400000 -f 1000 -q 1000" ]
    num_rows = int(400000/1000)


    all_processes = []
    # get 10 stream average for each generator
    gen_no = 4
    exp_dir = mcv.OUTPUT_DIR + "/" + str(24) 
    output_dirs = []
    for gen_string in generators:
      seeded_generators = []
      gen_no += 1
      output_dir = exp_dir + "/" + str(gen_no) 
      output_dirs.append(output_dir)

      for randomSeed in range(0, 10): #random seed for tree; generate 10 random streams  for this generator
        gen_cmd = re.sub("-r [0-9]+", "-r "+ str(randomSeed)+ " ", str(gen_string))
	#print(gen_cmd)
        seeded_generators.append(gen_cmd)

      seeded_experiments = se.CompositeExperiment.make_experiments(mcv.MOA_STUMP, evaluators, learners, seeded_generators)
      processes = se.CompositeExperiment.make_running_processes(seeded_experiments, output_dir)
      all_processes.extend(processes)

    exit_codes = [p.wait() for p in all_processes]
 
    # List of mean_dataframes
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
      for i in range(num_rows):
        all_stream_mean[i] = all_stream_learning_data[i::num_rows].mean()
      all_stream_mean_df = pd.DataFrame(all_stream_mean).transpose()
    #runexp24(learners, generators, evaluators, 24)
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
      error_df[" Classes: "+ os.path.basename(os.path.normpath(folder))+ " | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      #error_df[" | T: " + ("%.2f"%cpu_time) + 's | ' + " E:" + ("%.7f"%average_error) + ' |'] = all_stream_mean_df['error']
      split_df["splits" + os.path.basename(os.path.normpath(folder))] = all_stream_mean_df['splits']
      #error_df[str(folder)+" "+"5"] = all_stream_mean_df['error']

      mean_dataframes.append(all_stream_mean_df)

    # Set the index column
    # error_df[mcv.INDEX_COL]
    error_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    error_df = error_df.set_index(mcv.INDEX_COL)
    #error_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Error.csv")

    split_df[mcv.INDEX_COL] = mean_dataframes[0][mcv.INDEX_COL]
    split_df = split_df.set_index(mcv.INDEX_COL)
    #split_df.to_csv(mcv.OUTPUT_DIR + "/" + mcv.OUTPUT_PREFIX +  "Split.csv")

    #se.Plot.plot_df(error_df, " ", mcv.FIG_DIR+"/"+str(figNo).zfill(3), split_df)
    se.Plot.plot_df(error_df, "Error", mcv.FIG_DIR+"/"+str(24).zfill(3), split_df)




    # without the main sentinel below code will always get run, even when imported as a module!
if __name__=="__main__": 

    processes = {}
    #processes[1] = Process(target=chart1)
    #processes[2] = Process(target=chart2)
    #processes[3] = Process(target=chart3)
    #processes[4] = Process(target=chart4)
    #processes[5] = Process(target=chart5)
    #processes[6] = Process(target=chart6)
    #processes[7] = Process(target=chart7)
    #processes[8] = Process(target=chart8)
    #processes[9] = Process(target=chart9)
    #processes[10] = Process(target=chart10)
    #processes[11] = Process(target=chart11)
    #processes[12] = Process(target=chart12)
    #processes[13] = Process(target=chart13)

    #processes[14] = Process(target=chart14)
    #processes[15] = Process(target=chart15)
    #processes[16] = Process(target=chart16)
    #processes[17] = Process(target=chart17)

    #processes[18] = Process(target=chart18)
    #processes[19] = Process(target=chart19)
    #processes[20] = Process(target=chart20)
    #processes[21] = Process(target=chart21)
    #processes[22] = Process(target=chart22)


    #processes[23] = Process(target=chart23)
    processes[24] = Process(target=chart24)

    for key in processes:
      processes[key].start()
   
