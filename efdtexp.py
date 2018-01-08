
import simpleExperiments as se
import moa_command_vars as mcv
from multiprocessing import Process, Queue

def runexp1(learners, generators, evaluators, suffix):
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

def chart1():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/hepmass.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]

    runexp1(learners, generators, evaluators, 1)

def chart2():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/wisdmshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 2)

def chart3():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/susy.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 3)

def chart4():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/airlines.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 4)

def chart5():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/kddshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 5)

def chart6():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/higgsOrig.arff -c 33)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 6)

def chart7():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/poker-lsn.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 7)

def chart8():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/pokershuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 8)

def chart9():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/CovPokElec.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 9)

def chart10():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/cpeshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 10)

def chart11():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/covtypeNorm.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 11)

def chart12():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/covtypeshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 12)


def chart13():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/airlineshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 13)

def chart14():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3covtype.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 14)

def chart15():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3airlines.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 15)

def chart16():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3wisdm.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 16)

def chart17():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/3kdd.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 17)

def chart18():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/skinshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 18)


def chart19():

    learners = [ r"-l trees.VFDT", r"-l (trees.EFDT -R 2000)"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/pamap2_9subjectsshuf.arff -c 2)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 19)

def chart20():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/fontshuf.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 20)

def chart21():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/chessshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 21)

def chart22():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /mnt/datasets/chessshufdiscrete.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 10000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 22)


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
    processes[9] = Process(target=chart9)
    processes[10] = Process(target=chart10)
    processes[11] = Process(target=chart11)
    processes[12] = Process(target=chart12)
    processes[13] = Process(target=chart13)

    #processes[14] = Process(target=chart14)
    #processes[15] = Process(target=chart15)
    #processes[16] = Process(target=chart16)
    #processes[17] = Process(target=chart17)

    #processes[18] = Process(target=chart18)
    #processes[19] = Process(target=chart19)
    #processes[20] = Process(target=chart20)
    #processes[21] = Process(target=chart21)
    #processes[22] = Process(target=chart22)


    for key in processes:
      processes[key].start()
   
