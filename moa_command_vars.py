
#The parameter style in this file is different when the parameters correspond to MOAparameters directly (camel case vs underscores).

PREFIX = "/home/cman39/p2016030006/cman39"

from os.path import expanduser
HOME_DIR = expanduser("~")
RESULTS_DIR = "{prefix}/exp_dir_results".format(prefix = PREFIX)
DATA_DIR = "{prefix}/datasets".format(prefix = PREFIX)

#HOME_DIR = '/home/chait'
MOA_DIR = '{home_dir}/javacode/driftgen/dependency_jars'.format(home_dir = HOME_DIR)
OUTPUT_DIR = '{resultsDir}/output'.format(resultsDir = RESULTS_DIR)
#FIG_DIR = '{resultsDir}/figures'.format(resultsDir = RESULTS_DIR)
FIG_DIR = './figures'.format(resultsDir = RESULTS_DIR)
OUTPUT_PREFIX = 'out'

#MOA_STUMP = "java -cp commons-math3-3.6.1.jar:guava-22.0.jar:moa.jar:cdgen3.jar -javaagent:sizeofag-1.0.0.jar"
MOA_STUMP = "java -cp commons-math3-3.6.1.jar:guava-22.0.jar:moa.jar:mytrees.jar -ea -Xmx2g"

NUM_STREAMS = 10
INDEX_COL = 'learning evaluation instances'
FIELDS = """learning evaluation instances,evaluation time (cpu seconds),classified instances,classifications correct (percent),model training instances"""
FIELDS_AVG = """classifications correct (percent)"""
# broken with nonsensical values: model serialized size (bytes),model cost (RAM-Hours),model cost (RAM-Hours)
# splits is per evaluation period, so it makes no sense in the end fields, only for fields_avg

# java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar moa.gui.GUI

