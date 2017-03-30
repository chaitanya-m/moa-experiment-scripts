# Learners

MOA_LEARNER_PREFIX = "-l"

MOA_LEARNER_OPTION_NAIVE_BAYES = "moa.classifiers.bayes.NaiveBayes"
MOA_LEARNER_NAIVE_BAYES = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_NAIVE_BAYES])

MOA_LEARNER_OPTION_DECISION_STUMP = "moa.classifiers.trees.DecisionStump"
MOA_LEARNER_DECISION_STUMP = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_DECISION_STUMP])

MOA_LEARNER_OPTION_DRIFT_DETECTION_METHOD_CLASSIFIER = "moa.classifiers.drift.DriftDetectionMethodClassifier"
MOA_LEARNER_DRIFT_DETECTION_METHOD_CLASSIFIER = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_DRIFT_DETECTION_METHOD_CLASSIFIER])

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

MOA_LEARNER_OPTION_ACCURACY_UPDATED_ENSEMBLE = "moa.classifiers.meta.AccuracyUpdatedEnsemble"
MOA_LEARNER_ACCURACY_UPDATED_ENSEMBLE = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_ACCURACY_UPDATED_ENSEMBLE])

MOA_LEARNER_OPTION_ACCURACY_WEIGHTED_ENSEMBLE = "moa.classifiers.meta.AccuracyWeightedEnsemble"
MOA_LEARNER_ACCURACY_WEIGHTED_ENSEMBLE = " ".join([MOA_LEARNER_PREFIX, MOA_LEARNER_OPTION_ACCURACY_WEIGHTED_ENSEMBLE])

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
  def DecisionStumpLearnerBuilder():
    return Learner(MOA_LEARNER_DECISION_STUMP)

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

  @staticmethod
  def AccuracyUpdatedEnsembleLearnerBuilder():
    return Learner(MOA_LEARNER_ACCURACY_UPDATED_ENSEMBLE)

  @staticmethod
  def AccuracyWeightedEnsembleLearnerBuilder():
    return Learner(MOA_LEARNER_ACCURACY_WEIGHTED_ENSEMBLE)

  @staticmethod
  def DriftDetectionMethodClassifierLearnerBuilder():
    return Learner(MOA_LEARNER_DRIFT_DETECTION_METHOD_CLASSIFIER)

