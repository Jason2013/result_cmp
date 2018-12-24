# coding=utf-8

from enum import Enum
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


class TestResultTable(object):

    def __init__(self):
        self.headers = []
        self.data = []

    def AddHeader(header):
        self.headers.append(header)

    def AddDataRow(row):
        for (i, data) in enumerate(row):
            dataLen = len(data)
            if dataLen > self.headers[i].maxDataWidth:
                self.headers[i].maxDataWidth = dataLen
            if self.headers[i].dataType == ColumnDataType.Number:
                try:
                    val = float(row[i])
                    row[i] = val
                except ValueError:
                    if row[i] != "N/A":
                        self.headers[i].dataType = ColumnDataType.Text
        self.data.append(row)


class TestResult(object):

    def __init__(self, TestResultFile = None):
        self.testResultFile = TestResultFile if TestResultFile else None

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
                    state = RowState.ResultData
                elif state == RowState.ResultData:
                    if row:
                        print("Data: " + row)
                    else:
                        print("Misc: " + row)
                        state = RowState.ResultHeader
                else:
                    assert False


if __name__ == "__main__":
    r = TestResult(TEST_RESULTS_FILE)
    r.LoadData()
