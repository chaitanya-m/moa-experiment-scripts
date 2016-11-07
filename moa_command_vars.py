
#The parameter style in this file is different when the parameters correspond to MOAparameters directly (camel case vs underscores).

from os.path import expanduser
HOME_DIR = expanduser("~")



def setTrainingTestingParams(nInstances=None, testInterval=None, nTestExamples=None):

  cmd_options = ""

  if nInstances is not None:
    cmd_options += " -i {i_val} ".format(i_val = nInstances)

  if testInterval is not None:
    cmd_options += " -f {f_val}".format(f_val = testInterval)

  if nInstances is not None:
    cmd_options += " -q {q_val}".format(q_val = nTestExamples)

  return cmd_options

#HOME_DIR = '/home/chait'
MOA_DIR = '{home_dir}/moa-release-2016.04'.format(home_dir = HOME_DIR)
OUTPUT_DIR = '{home_dir}/exp_dir/output'.format(home_dir = HOME_DIR)
FIG_DIR = '{home_dir}/exp_dir/figures'.format(home_dir = HOME_DIR)
OUTPUT_PREFIX = 'out'

MOA_STUMP = "java -cp commons-math3-3.6.1.jar:moa.jar:cdgen3.jar -javaagent:sizeofag-1.0.0.jar"

num_instances = 400000
test_interval = 1000
num_test_examples = 1000

NUM_STREAMS = 5
INDEX_COL = 'learning evaluation instances'
NUM_ROWS = num_instances/test_interval

PARAMS = setTrainingTestingParams(num_instances, test_interval, num_test_examples)

# java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar moa.gui.GUI

