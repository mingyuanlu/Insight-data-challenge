"""Define class Data and the functions that read the window size and print out the average error to the assigned output file."""
import numpy as np
import Queue

def readWindowSize(windowSizeFile):
    """Read the window size from file"""
    with open(windowSizeFile) as f:
        return int(f.read())

def printAverageError(window, data, outputFile):
    """Use queue to compute the average error from merged data and print to outputFile."""
    error_digit = 2
    q_error = Queue.Queue(-1)
    q_count = Queue.Queue(window)
    with open(outputFile, "w") as f:

        for index in range(window):
            count = 0
            if(data.timeEntry[1][index] > 0):
                for index2 in range(len(data.mergedData[0])):
                    if (data.mergedData[0][index2] == data.timeEntry[0][index]):
                        q_error.put(data.mergedData[2][index2])
                        count++
                    elif (data.mergedData[0][index2] > data.timeEntry[0][index]):
                        break
                q_count.put(count)
            else:
                q_count.put(count)

        sum = np.sum(np.array(list(q_error.queue)))
        totalCount = np.sum(np.array(list(q_count.queue)))
        averageError = sum / float(totalCount)
        outstring = str(data.timeEntry[0][0])+'|'+str(data.timEntry[0][window-1])+'|'+str(np.round(averageError, error_digit))+'\n'
        f.write(outstring)

        for index in range(window, len(timeEntry[0])-window+1):
            count = 0
            if(data.timeEntry[1][index] > 0):
                for index2 in range(len(data.mergedData[0])):
                    if (data.mergedData[0][index2] == data.timeEntry[0][index]):
                        q_error.put(data.mergedData[2][index2])
                        count++
                    elif (data.mergedData[0][index2] > data.timeEntry[0][index]):
                        break
                q_count.put(count)
                for iteration in range(q_count.get()):
                    q_error.get()
            else:
                q_count.put(count)

            q_count.get()
            sum = np.sum(np.array(list(q_error.queue)))
            totalCount = np.sum(np.array(list(q_count.queue)))
            averageError = sum / float(totalCount)
            outstring = str(data.timeEntry[0][index-(window-1)])+'|'+str(data.timEntry[0][index])+'|'+str(np.round(averageError, error_digit))+'\n'


Class Data():
    """Read input data and merge data to a common table."""

    def __init__(self, trueDataFile, predictedDataFile):
        #self.trueDataFile = trueDataFile
        #self.predictedDataFile = predictedDataFile
        #trueData = readData(trueDataFile)
        #predictedData = readData(predictedDataFile)
        #timeEntry = getTimeEntry(predictedDataFile)
        self.mergedData, self.timeEntry = mergeData(trueDataFile, predictedDataFile)

    '''
    def readData(dataFile):
        """Read input text data delimited by "|"."""
        data = [[],[],[]]
        with open(dataFile) as f:
            for row in f:
                d = row.rstrip().split('|')
                data[0].append(d[0])
                data[1].append(d[1])
                data[2].append(d[2])

        return data
    '''

    def mergeData(trueDataFile, predictedDataFile):
        """Merge data from true and predicted tables into one single table, effectively doing a left merge (left being predicted)."""

        timeEntry = [[],[]]
        data = [[],[],[]]
        start_row = 0
        with open(predictedDataFile) as fpred:
            with open(trueDataFile) as ftrue:
                timeEntry[0].append(range(ftrue[0].rstrip().split('|')[0], ftrue[len(ftrue)-1].rstrip().split('|')[0]))
                timeEntry[1].append([0]*len(timeEntry[0]))
                for rowpred in fpred:
                    dpred = rowpred.rstrip().split('|')
                    hourpred  = int(dpred[0])
                    idpred    = dpred[1]
                    pricepred = float(dpred[2])
                    timeEntry[hourpred] = 1
                    for rowtrue in ftrue[start_row:]: #the data can be assumed to be in chronological order
                        dtrue = rowtrue.rstrip().split('|')
                        hourtrue  = int(dtrue[0])
                        idtrue    = dtrue[1]
                        pricetrue = float(dtrue[2])
                        start_row += 1
                        if(hourtrue == hourpred):
                            if(idtrue == idpred):
                                data[0].append(hourpred)
                                data[1].append(idpred)
                                data[2].append(np.fabs(pricepred-pricetrue))
                        elif hourtrue > hourpred:
                            break;

        return [data, timeEntry]

'''
Class Queue():
    """Queue input data with a fixed time range specified by "window"."""

    def __init__():

        self.price = []
        """
        sum = 0.
        count = 0
        for index in range(start_index, start_index+window):
            if(data.timEntry[1][index]):
                for id in data.mergedData[1]
        """
'''
