# Learners

MOA_LEARNER_PREFIX = "-l"

MOA_LEARNER_OPTION_NAIVE_BAYES = "moa.classifiers.bayes.NaiveBayes"
MOA_LEARNER_NAIVE_BAYES = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_NAIVE_BAYES])

MOA_LEARNER_OPTION_HOEFFDING_ADAPTIVE_TREE = "moa.classifiers.trees.HoeffdingAdaptiveTree"
MOA_LEARNER_HOEFFDING_ADAPTIVE_TREE = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_HOEFFDING_ADAPTIVE_TREE])

MOA_LEARNER_OPTION_HOEFFDING_OPTION_TREE = "moa.classifiers.trees.HoeffdingOptionTree"
MOA_LEARNER_HOEFFDING_OPTION_TREE = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_HOEFFDING_OPTION_TREE])

MOA_LEARNER_OPTION_HOEFFDING_TREE = "moa.classifiers.trees.HoeffdingTree"
MOA_LEARNER_HOEFFDING_TREE = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_HOEFFDING_TREE])

MOA_LEARNER_OPTION_OZA_BAG = "moa.classifiers.meta.OzaBag"
MOA_LEARNER_OZA_BAG = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_OZA_BAG])

MOA_LEARNER_OPTION_OZA_BOOST = "moa.classifiers.meta.OzaBoost"
MOA_LEARNER_OZA_BOOST = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_OZA_BOOST])

MOA_LEARNER_OPTION_OZA_BAG_ADWIN = "moa.classifiers.trees.OzaBagAdwin"
MOA_LEARNER_OZA_BAG_ADWIN = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_OZA_BAG_ADWIN])

MOA_LEARNER_OPTION_OZA_BOOST_ADWIN = "moa.classifiers.trees.OzaBoostAdwin"
MOA_LEARNER_OZA_BOOST_ADWIN = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_OZA_BOOST_ADWIN])

class Learner:

  def __init__(self, command):
    self.command = command
  def cmd(self):
    return self.command

class LearnerBuilder:

  @staticmethod
  def NaiveBayesLearnerBuilder():
    return Learner(MOA_LEARNER_NAIVE_BAYES)

  @staticmethod
  def HoeffdingAdaptiveLearnerBuilder():
    return Learner(MOA_LEARNER_HOEFFDING_ADAPTIVE_TREE)

  @staticmethod
  def HoeffdingOptionLearnerBuilder():
    return Learner(MOA_LEARNER_HOEFFDING_OPTION_TREE)

  @staticmethod
  def HoeffdingLearnerBuilder():
    return Learner(MOA_LEARNER_HOEFFDING_TREE)

  @staticmethod
  def OzaBagLearnerBuilder():
    return Learner(MOA_LEARNER_OZA_BAG)

  @staticmethod
  def OzaBoostLearnerBuilder():
    return Learner(MOA_LEARNER_OZA_BOOST)

  @staticmethod
  def OzaBagAdwinLearnerBuilder():
    return Learner(MOA_LEARNER_OZA_BAG_ADWIN)

  @staticmethod
  def OzaBoostAdwinLearnerBuilder():
    return Learner(MOA_LEARNER_OZA_BOOST_ADWIN)

