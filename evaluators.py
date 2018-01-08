# Evaluators

MOA_TASK_PREFIX = "moa.DoTask"

MOA_TASK_OPTION_EVALUATE_INTERLEAVED_TEST_THEN_TRAIN = "EvaluateInterleavedTestThenTrain"
MOA_TASK_OPTION_EITTT = "EvaluateInterleavedTestThenTrain"
MOA_TASK_EITTT = " ".join([MOA_TASK_PREFIX, MOA_TASK_OPTION_EITTT])

MOA_TASK_OPTION_EVALUATE_PREQUENTIAL = "EvaluatePrequential"
MOA_TASK_EVALUATE_PREQUENTIAL = " ".join([MOA_TASK_PREFIX, MOA_TASK_OPTION_EVALUATE_PREQUENTIAL])

MOA_TASK_OPTION_EVALUATE_PREQ_ADWIN = "AdwinClassificationPerformanceEvaluator"
MOA_TASK_EVALUATE_PREQ_ADWIN = " ".join([MOA_TASK_EVALUATE_PREQUENTIAL, " -e ", MOA_TASK_OPTION_EVALUATE_PREQ_ADWIN])


def setTrainingTestingParams(nInstances=None, testInterval=None, nTestExamples=None):

  cmd_options = ""

  if nInstances is not None:
    cmd_options += " -i {i_val} ".format(i_val = nInstances)

  if testInterval is not None:
    cmd_options += " -f {f_val}".format(f_val = testInterval)

  if nTestExamples is not None:
    cmd_options += " -q {q_val}".format(q_val = nTestExamples)

  return cmd_options

num_instances = 10000000
test_interval = 1000
num_test_examples = 1000

NUM_ROWS = num_instances/test_interval

PARAMS = setTrainingTestingParams(num_instances, test_interval, num_test_examples)

class Evaluator:

  def __init__(self, command):
    self.command = command + PARAMS
  def cmd(self):
    return self.command

class EvaluatorBuilder:

  @staticmethod
  def EvaluateInterleavedTestThenTrainBuilder():
    return Evaluator(MOA_TASK_EITTT)

  @staticmethod
  def EvaluatePrequentialBuilder():
    return Evaluator(MOA_TASK_EVALUATE_PREQUENTIAL)

  @staticmethod
  def EvaluatePrequentialAdwinBuilder():
    return Evaluator(MOA_TASK_EVALUATE_PREQ_ADWIN)
