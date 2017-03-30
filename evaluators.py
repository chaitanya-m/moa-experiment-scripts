# Evaluators

MOA_TASK_PREFIX = "moa.DoTask"


MOA_TASK_OPTION_EVALUATE_INTERLEAVED_TEST_THEN_TRAIN = "EvaluateInterleavedTestThenTrain"
MOA_TASK_OPTION_EITTT = "EvaluateInterleavedTestThenTrain"
MOA_TASK_EITTT = " ".join([MOA_TASK_PREFIX, MOA_TASK_OPTION_EITTT])

MOA_TASK_OPTION_EVALUATE_PREQUENTIAL = "EvaluatePrequential"
MOA_TASK_EVALUATE_PREQUENTIAL = " ".join([MOA_TASK_PREFIX, MOA_TASK_OPTION_EVALUATE_PREQUENTIAL])

MOA_TASK_OPTION_EVALUATE_PREQ_ADWIN = "AdwinClassificationPerformanceEvaluator"
MOA_TASK_EVALUATE_PREQ_ADWIN = " ".join([MOA_TASK_EVALUATE_PREQUENTIAL, " -e ", MOA_TASK_OPTION_EVALUATE_PREQ_ADWIN])

class Evaluator:

  def __init__(self, command):
    self.command = command
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
