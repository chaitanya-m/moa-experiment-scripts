# GeneratorBuilder, Generator classes

import re

MOA_GENERATOR_PREFIX = "-s"

MOA_GENERATOR_OPTION_ABRUPT_DRIFT = "generators.monash.AbruptDriftGenerator"
MOA_GENERATOR_ABRUPT_DRIFT = " ".join([MOA_GENERATOR_PREFIX, MOA_GENERATOR_OPTION_ABRUPT_DRIFT])

MOA_GENERATOR_OPTION_GRADUAL_DRIFT = "generators.monash.GradualDriftGenerator"
MOA_GENERATOR_GRADUAL_DRIFT = " ".join([MOA_GENERATOR_PREFIX, MOA_GENERATOR_OPTION_GRADUAL_DRIFT])

class Generator:

  def __init__(self, command):
    self.command = command
  def cmd(self):
    return self.command


class GeneratorBuilder:

  @staticmethod
  def MonashAbruptDriftGenBuilder(nAttributes=None, nValuesPerAttribute=None, burnIn=None, driftMagPrior=None, driftMagConditional=None, epsilon=None, driftConditional=False, driftPrior=False, randomSeed=None):

    # We assume that these values already have defaults in MOA and only change them on a case-by-case basis 
    gen_stump_begin = " -s \"\"\"(generators.monash.AbruptDriftGenerator "
    gen_stump_end = " )\"\"\" "
    gen_options = ""
    gen_cmd = ""

    if nAttributes is not None:
      gen_options += " -n {n_val}".format(n_val = nAttributes)

    if nValuesPerAttribute is not None:
      gen_options += " -v {v_val}".format(v_val = nValuesPerAttribute)

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

    return Generator(gen_cmd)



  @staticmethod
  def MonashGradualDriftGenBuilder(nAttributes=None, nValuesPerAttribute=None, burnIn=None, driftMagPrior=None, driftDuration=None, epsilon=None, randomSeed=None):

    # We assume that these values already have defaults in MOA and only change them on a case-by-case basis 
    gen_stump_begin = " -s \"\"\"(generators.monash.GradualDriftGenerator "
    gen_stump_end = " )\"\"\" "
    gen_options = ""
    gen_cmd = ""

    if nAttributes is not None:
      gen_options += " -n {n_val}".format(n_val = nAttributes)

    if nValuesPerAttribute is not None:
      gen_options += " -v {v_val}".format(v_val = nValuesPerAttribute)

    if burnIn is not None:
      gen_options += " -b {b_val} ".format(b_val = burnIn)

    if driftMagPrior is not None:
      gen_options += " -i {i_val} ".format(i_val = driftMagPrior)

    if driftDuration is not None:
      gen_options += " -d {d_val} ".format(d_val = driftDuration)

    if epsilon is not None:
      gen_options += " -e {e_val} ".format(e_val = epsilon)

    if randomSeed is not None:
      gen_options += " -r {r_val} ".format(r_val = randomSeed)

    gen_cmd = gen_stump_begin + gen_options + gen_stump_end

    return Generator(gen_cmd)


  @staticmethod
  def SimpleSeededGenBuilder(gen_string, randomSeed=None):

    # if random seed is not none, just substitute any -r options with the correct seed
    # the -r options must be clearly visible... 
    # imagine the amount of refactoring needed every time new options are added... that's too
    # much complexity for a piece of code custom-built to work with MOA.

    print("====" + str(gen_string))
    gen_cmd = " -s (" + re.sub("-r [0-9]+", "-r "+ str(randomSeed)+ " ", str(gen_string)) + " )"

    return Generator(gen_cmd)

