#!/bin/python

import sys
import numpy as np
import myModule

#arg 1: window file
#arg 2: true value file
#arg 3: predicted value file
#arg 4: output file

if (len(sys.argv) != 5):
    print("Expected 4 arguments. Now have: %d") % (len(sys.argv))
    return -1

windowSizeFile = sys.argv[1]
trueData       = sys.argv[2]
predictedData  = sys.argv[3]
outputFile     = sys.argv[4]

window = myModule.readWindowSize(windowSizeFile)
#need to check that there are at least "window" number of hours
data = myModule.Data(trueData, predictedData)
myModule.printAverageError(window, data, ouputFile)
