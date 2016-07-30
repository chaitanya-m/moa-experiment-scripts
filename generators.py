# GeneratorBuilder, Generator classes

MOA_GENERATOR_PREFIX = "-s"
MOA_GENERATOR_OPTION_ABRUPT_DRIFT = "generators.categorical.AbruptDriftGenerator"
MOA_GENERATOR_ABRUPT_DRIFT = " ".join([MOA_GENERATOR_PREFIX, MOA_GENERATOR_OPTION_ABRUPT_DRIFT])



class Generator:

  def __init__(self, command):
    self.command = command
  def cmd(self):
    return self.command

class GeneratorBuilder:

  @staticmethod
  def CategoricalAbruptDriftGenBuilder(nAttributes=None, nValuesPerAttribute=None, burnIn=None, driftMagPrior=None, driftMagConditional=None, epsilon=None, driftConditional=False, driftPrior=False, randomSeed=None):

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

    return Generator(gen_cmd)


