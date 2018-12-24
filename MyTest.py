# coding=utf-8

import unittest
import ResultTable

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

if __name__ == "__main__":
    unittest.main()
