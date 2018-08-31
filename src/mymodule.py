"""Define class Data and the functions that read the window size and print out the average error to the assigned output file."""
import numpy as np
import Queue
import sys

def read_window_size(window_size_file):
    """Read the window size from file"""

    with open(window_size_file) as f:

        data = f.read()
        try:
            val = int(data)
        except ValueError:
            print('Window size \'{}\' not an int!'.format(data))
            raise ValueError('Window size \'{}\' not an int!'.format(data))
            val = None

    return val


def make_dict(list):
    """Generate a dictionary from the list, where the key is the unique list element, and the value is the number count of the key."""

    array = np.array(list)
    unique, counts = np.unique(array, return_counts=True)
    return dict(zip(unique, counts))


def compute_average_error(q_error, q_count):
    """Compute the average error as the (sum of error)/(sum of counts)."""

    sum = np.sum(np.array(list(q_error.queue)))
    total_count = np.sum(np.array(list(q_count.queue)))
    if total_count == 0: # No match in window
        return None
    else:
        return sum / float(total_count)

def make_output_string(hour_start, hour_end, average_error, error_digit):
    """Generate otuput string according to the required format."""

    if average_error is None: # No match in window
        return str(hour_start)+'|'+str(hour_end)+'|NA\n'
    else:
        temp = '{0:.'+str(error_digit)+'f}'
        return str(hour_start)+'|'+str(hour_end)+'|'+temp.format(round(average_error,error_digit))+'\n'


def print_average_error(window, data, output_file):
    """Use queue to compute the average error from merged data and print to output_file."""

    error_digit = 2
    q_error = Queue.Queue(-1)
    q_count = Queue.Queue(window)
    counts_dict = make_dict(data.merged_data[0])

    start_row = 0

    with open(output_file, "w") as f:

        # If the window is not >= data time span
        if (window < len(data.time_entry[0])):
            for index in range(window):
                count = 0

                if(data.time_entry[1][index] > 0):
                    start_row += counts_dict[data.time_entry[0][index]]

                    for index2 in range(len(data.merged_data[0])):
                        if (data.merged_data[0][index2] == data.time_entry[0][index]):
                            q_error.put(data.merged_data[2][index2])
                            count+=1
                        elif (data.merged_data[0][index2] > data.time_entry[0][index]):
                            break
                    q_count.put(count)
                else:
                    q_count.put(count)

            average_error = compute_average_error(q_error, q_count) #sum / float(total_count)
            f.write(make_output_string(data.time_entry[0][0], data.time_entry[0][window-1], average_error, error_digit))

            # Slide the window
            for index in range(window, len(data.time_entry[0])):
                count = 0
                iteration_list = range(q_count.get())

                if(data.time_entry[1][index] > 0):
                    for index2 in range(start_row, len(data.merged_data[0])):
                        if (data.merged_data[0][index2] == data.time_entry[0][index]):
                            q_error.put(data.merged_data[2][index2])
                            count+=1
                        elif (data.merged_data[0][index2] > data.time_entry[0][index]):
                            break

                    q_count.put(count)

                    if data.time_entry[0][index] in counts_dict:
                        start_row += counts_dict[data.time_entry[0][index]]
                else:
                    q_count.put(count)

                # Dequeue
                for iter in iteration_list:
                    q_error.get()

                average_error = compute_average_error(q_error, q_count)
                f.write(make_output_string(data.time_entry[0][index-(window-1)], data.time_entry[0][index], average_error, error_digit))

        else: # If the window is >= data time span, only one average to compute
            for index in range(len(data.time_entry[0])):
                count = 0

                if(data.time_entry[1][index]>0):
                    for index2 in range(len(data.merged_data[0])):
                        if (data.merged_data[0][index2] == data.time_entry[0][index]):
                            q_error.put(data.merged_data[2][index2])
                            count+=1
                        elif (data.merged_data[0][index2] > data.time_entry[0][index]):
                            break
                    q_count.put(count)
                else:
                    q_count.put(count)

            average_error = compute_average_error(q_error, q_count) #sum / float(total_count)
            f.write(make_output_string(data.time_entry[0][0], data.time_entry[0][len(data.time_entry[0])-1], average_error, error_digit))



def read_line(row):
    """Read line from input file."""

    good_line = True # If True, this line contains valid data. Else, this line is skipped.
    data = row.rstrip().split('|')

    try:
        val = int(data[0])
    except ValueError:
        print("First column is not an int! This row will be skipped.")
        good_line = False
        #raise ValueError("First column is not an int! This row will be skipped.")

    try:
        val = float(data[2])
    except ValueError:
        print("Third column is not a float! This row will be skipped.")
        good_line = False
        #raise ValueError("Third column is not a float! This row will be skipped.")

    if (good_line):
        return [int(data[0]), data[1], float(data[2]), good_line]
    else:
        return [None, None, None, good_line]


class Data():
    """Read input data and merge data to a common table."""

    def __init__(self):
        pass
        #self.merged_data = []
        #self.time_entry  = []
        #self.merge_data(true_data_file, predicted_data_file)


    def merge_data(self, true_data_file, predicted_data_file):
        """Merge data from true and predicted tables into one single table, effectively doing a left merge (left being predicted)."""

        time_entry = []
        data = [[],[],[]]
        start_row = 0

        with open(predicted_data_file) as fpred:
            with open(true_data_file) as ftrue:
                ftrue_data = []
                ftrue_hour = []

                # Get actual data and its time span
                for line in ftrue:
                    hourtrue, idtrue, pricetrue, good_line = read_line(line)
                    if(good_line):
                        ftrue_data.append(line)
                        ftrue_hour.append(hourtrue)

                # The dictionary keeps track of how many rows are in each hour
                counts_dict = make_dict(ftrue_hour)
                # List of hours
                time_entry.append(range(ftrue_hour[0], ftrue_hour[len(ftrue_hour)-1]+1))
                # List of whether each hour has any matching actual/predicted pair
                time_entry.append([0]*len(time_entry[0]))

                for rowpred in fpred:
                    # Get predicted data
                    hourpred, idpred, pricepred, good_line = read_line(rowpred)
                    if(good_line):
                        # The existence of a predicted data entry ensures that there is a matching actual data entry, since predictions are filtered according to their confidence level, while actual data is not
                        time_entry[1][hourpred-int(time_entry[0][0])] = 1
                        passed_rows = 0

                        # Data is in chronological order, so can jump to the current hour to search for match
                        for hr in range(ftrue_hour[0], hourpred):
                            if hr in counts_dict:
                                passed_rows += counts_dict[hr]

                        for rowtrue in ftrue_data[passed_rows:]: #the data can be assumed to be in chronological order
                            hourtrue, idtrue, pricetrue, good_line = read_line(rowtrue)

                            # Locating the match
                            if(hourtrue == hourpred):
                                if(idtrue == idpred):
                                    data[0].append(hourpred)
                                    data[1].append(idpred)
                                    data[2].append(np.fabs(pricepred-pricetrue))

                            # Chronologically ordered data
                            elif hourtrue > hourpred:
                                break

        self.merged_data = data
        self.time_entry  = time_entry
