#!/bin/python

import sys
import numpy as np
import mymodule
from datetime import datetime

#arg 1: window file
#arg 2: true value file
#arg 3: predicted value file
#arg 4: output file

if (len(sys.argv) != 5):
    print("Expected 4 arguments. Now have: %d") % (len(sys.argv))
    sys.exit(1)

startTime = datetime.now()

window_size_file = sys.argv[1]
true_data        = sys.argv[2]
predicted_data   = sys.argv[3]
output_file      = sys.argv[4]

# Read window size
window = mymodule.read_window_size(window_size_file)
if window is None:
    exit(1)

# Read stock price data, and merge actual/predicted data
data = mymodule.Data()
data.merge_data(true_data, predicted_data)

# Slide window through merged data and obtain average errors
mymodule.print_average_error(window, data, output_file)

print datetime.now() - startTime
