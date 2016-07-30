# Evaluators

MOA_TASK_PREFIX = "moa.DoTask"
MOA_TASK_OPTION_EVALUATE_INTERLEAVED_TEST_THEN_TRAIN = "EvaluateInterleavedTestThenTrain"
MOA_TASK_OPTION_EITTT = "EvaluateInterleavedTestThenTrain"
MOA_TASK_EITTT = " ".join([MOA_TASK_PREFIX, MOA_TASK_OPTION_EITTT])


class Evaluator:

  def __init__(self, command):
    self.command = command
  def cmd(self):
    return self.command

class EvaluatorBuilder:

  @staticmethod
  def EvaluateInterleavedTestThenTrainBuilder():
    return Evaluator(MOA_TASK_EITTT)



