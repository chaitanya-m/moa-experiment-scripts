
#The parameter style in this file is different when the parameters correspond to MOAparameters directly (camel case vs underscores).

from os.path import expanduser
HOME_DIR = expanduser("~")

#HOME_DIR = '/home/chait'
MOA_DIR = '{home_dir}/execmoa'.format(home_dir = HOME_DIR)
OUTPUT_DIR = '{home_dir}/exp_dir/output'.format(home_dir = HOME_DIR)
FIG_DIR = '{home_dir}/exp_dir/figures'.format(home_dir = HOME_DIR)
OUTPUT_PREFIX = 'out'

#MOA_STUMP = "java -cp commons-math3-3.6.1.jar:guava-22.0.jar:moa.jar:cdgen3.jar -javaagent:sizeofag-1.0.0.jar"
MOA_STUMP = "java -cp commons-math3-3.6.1.jar:guava-22.0.jar:moa.jar:cdgen3.jar -ea -Xmx2g"

NUM_STREAMS = 10
INDEX_COL = 'learning evaluation instances'
FIELDS = """learning evaluation instances,evaluation time (cpu seconds),classified instances,classifications correct (percent),Kappa Statistic (percent),Kappa Temporal Statistic (percent),Kappa M Statistic (percent),model training instances,tree size (nodes),tree size (leaves),active learning leaves,tree depth,active leaf byte size estimate,inactive leaf byte size estimate"""
FIELDS_AVG = """classifications correct (percent),Kappa Statistic (percent),Kappa Temporal Statistic (percent),Kappa M Statistic (percent),tree size (nodes),tree size (leaves),active learning leaves,tree depth,active leaf byte size estimate,inactive leaf byte size estimate,splits"""
# broken with nonsensical values: model serialized size (bytes),model cost (RAM-Hours),model cost (RAM-Hours)
# splits is per evaluation period, so it makes no sense in the end fields, only for fields_avg

# java -cp commons-math3-3.6.1.jar:moa.jar:cdgen.jar -javaagent:sizeofag-1.0.0.jar moa.gui.GUI

