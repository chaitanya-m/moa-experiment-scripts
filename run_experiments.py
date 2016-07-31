#! /usr/bin/python

##############################################################################################################
#
# Chaitanya Manapragada
#
# Generates multiple streams using MOA, waits until generation is completed, then averages data for all the streams
#
# Bug? Note that the "evaluation instances" field also gets averaged!!
# Also, the result has rows and columns swapped.
#
# By default a different random seed seems to be picked by the Categorical Abrupt Drift Generator for each stream.
# 
# Note that this can be refactored to not use output csv files at all, only using dataframes. However, my computer
# doesn't have enough memory. Perhaps this is a much faster solution for the computing grid provided enough RAM.
#
# Also note that the number of data frames in play can be cut drastically by having a running average.
# Should Experiment be initialised with processes? 
##############################################################################################################

import experiments as exp


def main():

  exp.ExperimentRunner.runExperiments()
  return 0


if __name__=="__main__":

  main()


# http://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
# https://docs.python.org/3.4/library/subprocess.html
# http://stackoverflow.com/questions/2331339/piping-output-of-subprocess-popen-to-files
# http://stackoverflow.com/questions/24765017/how-to-calculate-average-of-numbers-from-multiple-csv-files
# http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
# http://stackoverflow.com/questions/4555932/public-or-private-attribute-in-python-what-is-the-best-way
# http://unix.stackexchange.com/questions/43478/vi-vim-how-can-i-write-out-a-number-of-lines-to-a-new-file
