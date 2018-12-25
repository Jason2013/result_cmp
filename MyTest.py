# coding=utf-8

import unittest
import pickle

import ResultTable
from ResultTable import *

class TestColumnHeader(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        x = ResultTable.ColumnHeader("header")
        self.assertEqual(x.caption, "header")
        self.assertEqual(x.columnWidth, 1)
        self.assertEqual(x.dataType, ResultTable.ColumnDataType.Number)
        self.assertEqual(x.maxDataWidth, 1)


class TestResultTable(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compatible(self):
        TEST_RESULTS_FILE = r"data\shaderbench\Ariel_llpc\1\001\test_results.txt"
        r1 = ResultTable.TestResult(TEST_RESULTS_FILE)
        r1.LoadData()
        # r2 = ResultTable.TestResult(TEST_RESULTS_FILE)
        # r2.LoadData()
        # self.assertTrue(r1.tabs[0].Compatible(r2.tabs[0]))
        with open("TestResult_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
            r3 = pickle.load(f)
            self.assertTrue(r1.tabs[0].Compatible(r3.tabs[0]))

    def test_copy(self):
        TEST_RESULTS_FILE = r"data\shaderbench\Ariel_llpc\1\001\test_results.txt"
        r1 = ResultTable.TestResult(TEST_RESULTS_FILE)
        r1.LoadData()
        # r2 = ResultTable.TestResult(TEST_RESULTS_FILE)
        # r2.LoadData()
        # self.assertTrue(r1.tabs[0].Compatible(r2.tabs[0]))
        with open("TestResult_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
            r3 = pickle.load(f)
            self.assertTrue(r1.tabs[0].Compatible(r3.tabs[0]))


if __name__ == "__main__":
    unittest.main()
