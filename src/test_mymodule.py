#!/bin/python

import unittest
import sys
import os
import Queue
from mymodule import *
import filecmp

class DataTest(unittest.TestCase):
    """Test class Data."""

    def get_script_path(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def setUp(self):
        """Define data used in test."""

        self.merged_data = [[1, 1, 1, 1, 2, 2, 3, 3, 3], ['ATAYJP', 'HVIWZR', 'SLKWVA', 'CMWTQH', 'ATAYJP', 'HVIWZR', 'ATAYJP', 'HVIWZR', 'SLKWVA'], [0.029999999999997584, 0.00999999999999801, 0.020000000000010232, 0.04999999999999716, 0.3000000000000007, 0.08999999999999986, 0.08999999999999986, 0.120000000000001, 1.4799999999999898]]
        self.time_entry = [[1, 2, 3], [1, 1, 1]]
        pwd = self.get_script_path()
        self.true_data_file = pwd+'/../insight_testsuite/tests/my_test/input/actual.txt'
        self.predicted_data_file = pwd+'/../insight_testsuite/tests/my_test/input/predicted.txt'

    def test_merge_data(self):
        """Merged data is as expected."""

        expected_data = self.merged_data
        expected_time_entry = self.time_entry
        temp_data = Data()
        temp_data.merge_data(self.true_data_file, self.predicted_data_file)
        self.assertEqual(sorted(temp_data.merged_data), sorted(self.merged_data))
        self.assertEqual(sorted(temp_data.time_entry), sorted(self.time_entry))



class MyModuleTest(unittest.TestCase):
    """Test functions in myModule."""

    def get_script_path(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def setUp(self):
        """Define data used in test."""

        pwd = self.get_script_path()
        self.window_size_file                    = pwd+'/../insight_testsuite/tests/my_test/input/window.txt'
        self.window_size_file_corrupted          = pwd+'/../insight_testsuite/tests/my_test/input/window_corrupted.txt'
        self.true_data_file                      = pwd+'/../insight_testsuite/tests/my_test/input/actual.txt'
        #self.true_data_file_corrupted_hour       = pwd+'/../insight_testsuite/tests/my_test/input/actual_corrupted_1.txt'
        #self.true_data_file_corrupted_price      = pwd+'/../insight_testsuite/tests/my_test/input/actual_corrupted_2.txt'
        self.predicted_data_file                 = pwd+'/../insight_testsuite/tests/my_test/input/predicted.txt'
        #self.predicted_data_file_corrupted_hour  = pwd+'/../insight_testsuite/tests/my_test/input/predicted_corrupted_1.txt'
        #self.predicted_data_file_corrupted_price = pwd+'/../insight_testsuite/tests/my_test/input/predicted_corrupted_2.txt'
        self.comparison_file                     = pwd+'/../insight_testsuite/tests/my_test/input/comparison.txt'


    def test_read_window_size(self):
        """Window size value is read correctly."""

        expected_window_size = 2
        window_size = read_window_size(self.window_size_file)
        self.assertEqual(expected_window_size, window_size)
        #print("corrupted: %s") % (self.window_size_file_corrupted)
        #Should raise value error when the supplied string cannot be converted to an integer.
        with self.assertRaises(ValueError):
            window_size = read_window_size(self.window_size_file_corrupted)
        #self.assertRaises(ValueError, read_window_size, self.window_size_file_corrupted)

    def test_make_dict(self):
        """Dictionary is correctly constructed according to the given list."""

        list = [1]*10 + [2]*5 + [17]*17
        dict1 = {1:10, 2:5, 17:17}
        dict2 = make_dict(list)
        self.assertEqual(dict1, dict2)

    def test_compute_average_error(self):
        """Error is correctly reported from the error and count queues, including when there is no count."""

        q_error = Queue.Queue(-1)
        q_count = Queue.Queue(-1)
        q_count_zeros = Queue.Queue(-1)
        for x in range(3):
            q_error.put(x)
            q_count.put(1)
            q_count_zeros.put(0)
        expected_average_error = 1.0
        average_error = compute_average_error(q_error, q_count)
        self.assertAlmostEqual(expected_average_error, average_error)

        #Check when the total number of counts is zero, the function returns None
        expected_average_error = None
        average_error = compute_average_error(q_error, q_count_zeros)
        self.assertIs(expected_average_error, average_error)


    def test_make_output_string(self):
        """The output string is properly formatted."""

        expected_output_string = '0|100|0.50\n'
        output_string = make_output_string(0,100,0.499,2)
        self.assertEqual(expected_output_string, output_string)

        expected_output_string = '1|200|NA\n'
        output_string = make_output_string(1,200,None,2)
        self.assertEqual(expected_output_string, output_string)

    def test_print_average_error(self):
        """The output file containing the errors is as expected."""

        window = read_window_size(self.window_size_file)
        temp_data = Data()
        temp_data.merge_data(self.true_data_file, self.predicted_data_file)
        expectedt_output_file = self.comparison_file
        pwd = self.get_script_path()
        output_file = pwd + '/../insight_testsuite/tests/my_test/output/comparison.txt'
        print temp_data
        print_average_error(window, temp_data, output_file)
        self.assertTrue(filecmp.cmp(expectedt_output_file, output_file))

    def test_read_line(self):
        """Line is correctly split."""

        expected_data = [0,'KITTEN',5.20]
        input_string = '0|KITTEN|5.20\n'
        data = read_line(input_string)
        self.assertEqual(expected_data[0], data[0])
        self.assertEqual(expected_data[1], data[1])
        self.assertAlmostEqual(expected_data[2], data[2])

        input_string = 'a|PARROT|3.31'
        #with self.assertRaises(ValueError):
        data = read_line(input_string)
        self.assertFalse(data[3])

        input_string = '1|BELUGA|4hjd'
        #with self.assertRaises(ValueError):
        data = read_line(input_string)
        self.assertFalse(data[3])


if __name__ == '__main__':
    unittest.main()
