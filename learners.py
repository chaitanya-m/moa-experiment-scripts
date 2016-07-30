# Learners

MOA_LEARNER_PREFIX = "-l"
MOA_LEARNER_OPTION_NAIVE_BAYES = "moa.classifiers.bayes.NaiveBayes"
MOA_LEARNER_NAIVE_BAYES = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_NAIVE_BAYES])

class Learner:

  def __init__(self, command):
    self.command = command
  def cmd(self):
    return self.command

class LearnerBuilder:

  @staticmethod
  def NaiveBayesLearnerBuilder():
    return Learner(MOA_LEARNER_NAIVE_BAYES)


