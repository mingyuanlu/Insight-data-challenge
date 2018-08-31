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

Unit tests can be run by

   $ python src/test_mymodule.py

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
s|YYAGBD|4.31
```
, then that stock entry will be skipped.

3. Invalid prices
Similar to the above case, if the price entry is not convertible to a float, such as
```
1|YYAGBD|8xc99
```
, then that stock entry will also be skipped.

4. No matched data
If no matching actual and predicted stock pairs are found in a time window, the output average error for that window will be 'NA'

5. Large time window
If the specified time window is equal to or larger than the time span of the stock data, only one average needs to be computed, namely the average of all matching price pairs in full data. The output line will have an ending hour equal to the last hour of actual data. For example, if the time window is 5 hours, the data starts at hour = 1 and ends at hour = 3. The average error is 0.24. The output will be
```
1|3|0.24
```
