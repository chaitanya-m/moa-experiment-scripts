
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
      r"-s (ArffFileStream -f /home/mchait/Downloads/hepmass.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]

    runexp1(learners, generators, evaluators, 1)

def chart2():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/wisdmshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 2)

def chart3():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/susy.arff -c 1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 3)

def chart4():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/airlines.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 4)

def chart5():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/kddshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 5)

def chart6():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/higgsOrig.arff -c 33)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 6)

def chart7():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/poker-lsn.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 7)

def chart8():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/pokershuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 8)

def chart9():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/CovPokElec.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 9)

def chart10():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/cpeshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 10)

def chart11():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/covtypeNorm.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 11)

def chart12():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/covtypeshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 12)


def chart13():

    learners = [ r"-l trees.VFDT", r"-l trees.EFDT"]
    generators = [
      r"-s (ArffFileStream -f /home/mchait/Downloads/airlineshuf.arff -c -1)"
    ]
    evaluators = [ r"EvaluatePrequential -i 7000000 -f 1000 -q 1000"]
    runexp1(learners, generators, evaluators, 13)





    # without the main sentinel below code will always get run, even when imported as a module!
if __name__=="__main__": 

   
    p1 = Process(target=chart1)
    p2 = Process(target=chart2)
    p3 = Process(target=chart3)
    p4 = Process(target=chart4)
    p5 = Process(target=chart5)
    p6 = Process(target=chart6)
    p7 = Process(target=chart7)
    p8 = Process(target=chart8)
    p9 = Process(target=chart9)
    p10 = Process(target=chart10)
    p11 = Process(target=chart11)
    p12 = Process(target=chart12)


    p1.start()
       #p2.start()
    #p3.start()
    p4.start()
       #p5.start()
       #p6.start()
       #p7.start()
       #  p8.start()
    #p9.start()
    #p10.start()
       #p11.start()
       #p12.start()

