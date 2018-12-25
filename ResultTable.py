# coding=utf-8

from enum import Enum
import sys

class RowState(Enum):
    Misc = 1
    ResultHeader = 2
    ResultData = 3
    ResultEnd = 4

class ColumnDataType(Enum):
    Text = 1
    Number = 2

TEST_RESULTS_FILE = r"D:\work\dev\teamcity\data\shaderbench\Ariel_llpc\1\001\test_results.txt"


class ColumnHeader(object):

    def __init__(self, caption, columnWidth = 1, dataType = ColumnDataType.Number, maxDataWidth = 1):
        self.caption = caption
        self.columnWidth = columnWidth
        self.dataType = dataType
        self.maxDataWidth = maxDataWidth

    def __str__(self):
        return "(%s, %d, %s, %d)" % (self.caption, self.columnWidth, "Number" if self.dataType == ColumnDataType.Number else "Text", self.maxDataWidth)

    def __eq__(self, other):
        return self.caption == other.caption \
            and self.columnWidth == other.columnWidth \
            and self.dataType == other.dataType \
            and self.maxDataWidth == self.maxDataWidth

    def __ne__(self, other):
        return not self.__eq__(other)


class TestResultTable(object):

    def __init__(self):
        self.headers = []
        self.data = []

    def AddHeader(self, header):
        self.headers.append(header)

    def AddHeadersFromStr(self, s):
        assert not self.headers
        for (caption, colWidth, maxDataWidth) in ((x.strip(), len(x), len(x.strip())) for x in s.split(",")):
            dataType = ColumnDataType.Text if caption in ("TestCaseId#", "API") else ColumnDataType.Number
            header = ColumnHeader(caption, colWidth, dataType, maxDataWidth)
            # self.headers.append(header)
            self.AddHeader(header)

    def AddDataRow(self, row):
        for (i, data) in enumerate(row):
            dataLen = len(data)
            if dataLen > self.headers[i].maxDataWidth:
                self.headers[i].maxDataWidth = dataLen
            if self.headers[i].dataType == ColumnDataType.Number and row[i] != "N/A":
                try:
                    val = float(row[i])
                    row[i] = val
                except ValueError:
                    self.headers[i].dataType = ColumnDataType.Text
        self.data.append(row)

    def Compatible(self, tab):
        if len(self.headers) != len(tab.headers):
            print("The header count is not equal!", file=sys.stderr)
            return False
        # for (lhs, rhs) in zip(
        err = next(((lhs, rhs) for (lhs, rhs) in zip(self.headers, tab.headers) if lhs != rhs), None)
        if err:
            print("The header %s is not equal to header %s!" % (lhs, rhs), file=sys.stderr)
            return False

        if len(self.data) != len(tab.data):
            print("The row count %d is not equal to row count %d!" % (len(self.data), len(tab.data)), file=sys.stderr)
            return False

        return True


class TestResult(object):

    def __init__(self, TestResultFile = None):
        self.testResultFile = TestResultFile if TestResultFile else None
        self.tabs = []

    def LoadData(self):
        state = RowState.Misc
        tab = None
        with open(self.testResultFile) as f:
            for row in (x.rstrip() for x in f):
                if state == RowState.Misc:
                    print("Misc: " + row)
                    if row.startswith("["):
                        pass
                    elif not row:
                        state = RowState.ResultHeader
                    else:
                        assert False
                elif state == RowState.ResultHeader:
                    assert row
                    print("Head: " + row)
                    tab = TestResultTable()
                    tab.AddHeadersFromStr(row)

                    state = RowState.ResultData
                elif state == RowState.ResultData:
                    if row:
                        print("Data: " + row)
                        tab.AddDataRow([x.strip() for x in row.split(",")])
                    else:
                        self.tabs.append(tab)
                        print("Misc: " + row)
                        state = RowState.ResultHeader
                else:
                    assert False
            self.tabs.append(tab)


class AvgTestResult(object):

    def __init__(self, results):
        pass

if __name__ == "__main__":
    r = TestResult(TEST_RESULTS_FILE)
    r.LoadData()
    print(r.tabs[0])
    for x in r.tabs[0].headers:
        print(x)
    for x in r.tabs[0].data:
        print(x)
