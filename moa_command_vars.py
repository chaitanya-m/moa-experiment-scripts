
#The parameter style in this file is different when the parameters correspond to MOAparamters directly (camel case vs underscores).

HOME_DIR = '/home/chait'
MOA_DIR = '{home_dir}/moa-release-2016.04'.format(home_dir = HOME_DIR)
OUTPUT_DIR = '{home_dir}/exp_dir/output'.format(home_dir = HOME_DIR)
OUTPUT_PREFIX = 'out'

MOA_STUMP = "java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar"


def setTrainingTestingParams(nInstances=None, testInterval=None, nTestExamples=None):

  cmd_options = ""

  if nInstances is not None:
    cmd_options += " -i {i_val} ".format(i_val = nInstances)

  if testInterval is not None:
    cmd_options += " -f {f_val}".format(f_val = testInterval)

  if nInstances is not None:
    cmd_options += " -q {q_val}".format(q_val = nTestExamples)

  return cmd_options

# java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar moa.gui.GUI



