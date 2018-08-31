# Table of Contents
1. [Dependencies](README.md#dependencies)
1. [Approach](README.md#approach)
1. [Run Instructions](README.md#run-instructions)
1. [Data Edge Case Handling](README.md#data-edge-case-handling)

--------

This is a project that compares hourly real-time stock prices to the prices predictions. The finial output consists of a listing of average deviation of the prediction as a function of a sliding time window. This project is based on the data challenge from Insight.

--------

## Dependencies

1. Python 2.7 or above
2. Python standard library
3. NumPy


## Approach

The actual and predicted stock price data, assuming both ordered chronologically, are read into two-dimensional tables respectively. A left-merge is then performed with the prediction as the left table. A sliding time window is applied on this merged table to calculate the average error (deviation) of all matching stocks within the window. To accelerate this computation, a queue data structure is used to take advantage of its FIFO property. This way, each time the window slides we only need to update the average with the enqueued data, minus the dequeued data.


## Run Instructions

The program can be simply run with

   $ sh run.sh

This will use the input data from /input/. If one wishes to pass different input data to the program, generally one can do

   $ python ./src/prediction-validation.py ${PATH-TO-WINDOW-SIZE-FILE} ${PATH-TO-ACTUAL-DATA} ${PATH-TO-PREDICTED-DATA} ${PATH-TO-OUTPUT-FILE}


## Data Edge Case Handling

Several edge cases for the input data are treated. They are

1. Invalid time window size
If the string stored in the window size file is not convertible to an integer, such as
```
a
```
, then the script will give an error and abort, since no sliding window can be defined.

2. Invalid hour
If the string stored in place of the hour entry in either the actual or predicted data is not convertible to an integer, such as
```
s
```
, then that stock entry will be skipped.

3. Invalid prices
Similar to the above case, if the price entry is not convertible to a float, such as
```
8xc99
```
, then that stock entry will also be skipped.

4. If no matching actual and predicted stock pairs are found in a time window, the output average error for that window will be 'NA'
