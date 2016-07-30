
HOME_DIR = '/home/chait'
MOA_DIR = '{home_dir}/moa-release-2016.04'.format(home_dir = HOME_DIR)
OUTPUT_DIR = '{home_dir}/exp_dir/output'.format(home_dir = HOME_DIR)
OUTPUT_PREFIX = 'out'

MOA_STUMP = "java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar"

MOA_TASK_PREFIX = "moa.DoTask"
MOA_LEARNER_PREFIX = "-l"
MOA_GENERATOR_PREFIX = "-s"

MOA_TASK_OPTION_EVALUATE_INTERLEAVED_TEST_THEN_TRAIN = "EvaluateInterleavedTestThenTrain"
MOA_TASK_OPTION_EITTT = "EvaluateInterleavedTestThenTrain"
MOA_TASK_EITTT = " ".join([MOA_TASK_PREFIX, MOA_TASK_OPTION_EITTT])

MOA_LEARNER_OPTION_NAIVE_BAYES = "moa.classifiers.bayes.NaiveBayes" 
MOA_LEARNER_NAIVE_BAYES = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_NAIVE_BAYES]) 

MOA_GENERATOR_OPTION_ABRUPT_DRIFT = "generators.categorical.AbruptDriftGenerator"
MOA_GENERATOR_ABRUPT_DRIFT = " ".join([MOA_GENERATOR_PREFIX, MOA_GENERATOR_OPTION_ABRUPT_DRIFT])

# Generator portion of the command
def CategoricalAbruptDriftGenCmd(nAttributes=None, nValuesPerAttribute=None, burnIn=None, driftMagPrior=None, driftMagConditional=None, epsilon=None, driftConditional=False, driftPrior=False, randomSeed=None):

  # We assume that these values already have defaults in MOA and only change them on a case-by-case basis 
  gen_stump_begin = " -s \"\"\"(generators.categorical.AbruptDriftGenerator "
  gen_stump_end = " )\"\"\" "
  gen_options = "" 
  gen_cmd = ""

  if burnIn is not None:
    gen_options += " -b {b_val} ".format(b_val = burnIn)

  if driftMagPrior is not None:
    gen_options += " -i {i_val} ".format(i_val = driftMagPrior)

  if driftMagConditional is not None:
    gen_options += " -o {o_val} ".format(o_val = driftMagConditional)

  if epsilon is not None:
    gen_options += " -e {e_val} ".format(e_val = epsilon)

  if driftConditional is True:
    gen_options += " -c "
    
  if driftPrior is True:
    gen_options += " -p "

  if randomSeed is not None:
    gen_options += " -r {r_val} ".format(r_val = randomSeed)

  gen_cmd = gen_stump_begin + gen_options + gen_stump_end

  return gen_cmd

# java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar moa.gui.GUI



