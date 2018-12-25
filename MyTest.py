# coding=utf-8

import copy
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


class TestUtils(unittest.TestCase):

    def test_avg_val(self):

        vals = [0.1, 0.1, 0.1, 2, 3]
        r = AvgVal(vals)
        self.assertTrue(r >= 0.1 - 1e-7 and r<= 0.1 + 1e-7)

        vals = [0.1, 0.1, 0.1, -2, 3]
        r = AvgVal(vals)
        self.assertTrue(r >= 0.1 - 1e-7 and r<= 0.1 + 1e-7)

        vals = [0.1, 0.1, 0.1, -2, -3]
        r = AvgVal(vals)
        self.assertTrue(r >= 0.1 - 1e-7 and r<= 0.1 + 1e-7)

        vals = [20.56214, 20.56206, 20.56187, 20.56204, 20.56210]
        r = AvgVal(vals)
        # print(r)
        self.assertTrue(r > 20.56206 and r< 20.56207)


    def test_avg_test_result_table(self):
        r = {}
        TEST_RESULTS_FILE = r"data\shaderbench\Ariel_llpc\{}\001\test_results.txt"
        for i in range(1, 6):
            r[i] = TestResult(TEST_RESULTS_FILE.format(i))
            r[i].LoadData()

        tabs = [tab.tabs[0] for tab in r.values()]

        res = AvgTestResultTable(tabs)

        # print(res.TableLines())
        s = res.TableLines()

        # with open("TestResultTable_data_shaderbench_Ariel_llpc_1-5_001_test_results.txt", "wb") as f:
        #     pickle.dump(s, f)

        with open("TestResultTable_data_shaderbench_Ariel_llpc_1-5_001_test_results.txt", "rb") as f:
            s1 = pickle.load(f)

        self.assertEqual(s, s1)

        # with open("TestResult_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
        #     r3 = pickle.load(f)
        #     self.assertTrue(r[1].Compatible(r3))

        # for (a, b) in ((i, j) for j in range(1,6) for i in range(1,6) if i != j):
        #     self.assertTrue(r[a].Compatible(r[b]))


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

        r2 = copy.deepcopy(r1)
        # r2 = ResultTable.TestResult(TEST_RESULTS_FILE)
        # r2.LoadData()
        # self.assertTrue(r1.tabs[0].Compatible(r2.tabs[0]))
        with open("TestResult_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
            r3 = pickle.load(f)
            self.assertTrue(r2.tabs[0].Compatible(r3.tabs[0]))

    def test_src_data_compatible(self):
        r = {}
        TEST_RESULTS_FILE = r"data\shaderbench\Ariel_llpc\{}\001\test_results.txt"
        for i in range(1, 6):
            r[i] = TestResult(TEST_RESULTS_FILE.format(i))
            r[i].LoadData()

        with open("TestResult_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
            r3 = pickle.load(f)
            self.assertTrue(r[1].tabs[0].Compatible(r3.tabs[0]))

        for (a, b) in ((i, j) for j in range(1,6) for i in range(1,6) if i != j):
            self.assertTrue(r[a].tabs[0].Compatible(r[b].tabs[0]))


    def test_src_result_compatible(self):
        r = {}
        TEST_RESULTS_FILE = r"data\shaderbench\Ariel_llpc\{}\001\test_results.txt"
        for i in range(1, 6):
            r[i] = TestResult(TEST_RESULTS_FILE.format(i))
            r[i].LoadData()

        with open("TestResult_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
            r3 = pickle.load(f)
            self.assertTrue(r[1].Compatible(r3))

        for (a, b) in ((i, j) for j in range(1,6) for i in range(1,6) if i != j):
            self.assertTrue(r[a].Compatible(r[b]))


    def test_avg_test_result_table_str(self):

        TEST_RESULTS_FILE = r"data\shaderbench\Ariel_llpc\1\001\test_results.txt"
        res = TestResult(TEST_RESULTS_FILE)
        res.LoadData()

        s = res.tabs[0].TableLines()

        # with open("TestResultTable_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "wb") as f:
        #     pickle.dump(s, f)

        with open("TestResultTable_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
            s1 = pickle.load(f)

        self.assertEqual(s, s1)


    def test_avg_test_result_str(self):

        TEST_RESULTS_FILE = r"data\shaderbench\Ariel_llpc\1\001\test_results.txt"
        res = TestResult(TEST_RESULTS_FILE)
        res.LoadData()

        s = res.ResultLines()

        # with open("TestResultTable_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "wb") as f:
        #     pickle.dump(s, f)

        with open("TestResultTable_data_shaderbench_Ariel_llpc_1_001_test_results.txt", "rb") as f:
            s1 = pickle.load(f)

        self.assertEqual(s, s1)


if __name__ == "__main__":
    unittest.main()
