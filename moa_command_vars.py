
HOME_DIR = '/home/chait'
MOA_DIR = '{home_dir}/moa-release-2016.04'.format(home_dir = HOME_DIR)
OUTPUT_DIR = '{home_dir}/exp_dir/output'.format(home_dir = HOME_DIR)
OUTPUT_PREFIX = 'out'

MOA_STUMP = "java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar"

MOA_TASK_PREFIX = "moa.DoTask"
MOA_LEARNER_PREFIX = "-l"

MOA_TASK_OPTION_EVALUATE_INTERLEAVED_TEST_THEN_TRAIN = "EvaluateInterleavedTestThenTrain"
MOA_TASK_OPTION_EITTT = "EvaluateInterleavedTestThenTrain"
MOA_TASK_EITTT = " ".join([MOA_TASK_PREFIX, MOA_TASK_OPTION_EITTT])

MOA_LEARNER_OPTION_NAIVE_BAYES = "moa.classifiers.bayes.NaiveBayes" 
MOA_LEARNER_NAIVE_BAYES = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_NAIVE_BAYES]) 


