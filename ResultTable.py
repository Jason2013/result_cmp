# coding=utf-8

from enum import Enum
import copy
import sys


class RowState(Enum):
    Misc = 1
    ResultHeader = 2
    ResultData = 3
    ResultEnd = 4


class ColumnDataType(Enum):
    Text = 1
    Number = 2


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

    def HeadLine(self):
        return ','.join([header.caption.rjust(header.columnWidth, " ") for header in self.headers])

    def AddHeadersFromStr(self, s):
        assert not self.headers
        for (caption, colWidth, maxDataWidth) in ((x.strip(), len(x), len(x.strip())) for x in s.split(",")):
            dataType = ColumnDataType.Text if caption in ("TestCaseId#", "API") else ColumnDataType.Number
            header = ColumnHeader(caption, colWidth, dataType, maxDataWidth)
            # self.headers.append(header)
            self.AddHeader(header)

    def AddDataRow(self, row):
        assert len(row) == len(self.headers)
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

    def DataRowLine(self, row):

        def ValueStr(val, dataType):

            if dataType == ColumnDataType.Text or val == "N/A":
                return val

            return "{:.5f}".format(val)


        return ','.join([ValueStr(col, header.dataType).rjust(header.columnWidth, " ") for (header, col) in zip(self.headers, row)])

    def TableLines(self):
        lines = [self.HeadLine()]
        for line in self.data:
            lines.append(self.DataRowLine(line))

        return '\n'.join(lines)

    def Compatible(self, tab):
        if len(self.headers) != len(tab.headers):
            print("The header count is not equal!", file=sys.stderr)
            return False

        for (lhs, rhs) in zip(self.headers, tab.headers):
            if lhs != rhs:
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
                    # print("Misc: " + row)
                    if row.startswith("["):
                        pass
                    elif not row:
                        state = RowState.ResultHeader
                    else:
                        assert False
                elif state == RowState.ResultHeader:
                    assert row
                    # print("Head: " + row)
                    tab = TestResultTable()
                    tab.AddHeadersFromStr(row)

                    state = RowState.ResultData
                elif state == RowState.ResultData:
                    if row:
                        # print("Data: " + row)
                        tab.AddDataRow([x.strip() for x in row.split(",")])
                    else:
                        self.tabs.append(tab)
                        # print("Misc: " + row)
                        state = RowState.ResultHeader
                else:
                    assert False
            self.tabs.append(tab)


    def Compatible(self, other):

        for (lhs, rhs) in zip(self.tabs, other.tabs):
            if not lhs.Compatible(rhs):
                return False

        return True

    def ResultLines(self):
        return '\n\n'.join([tab.TableLines() for tab in self.tabs])


def AvgVal(vals):

    assert len(vals) == 5

    for val in vals:
        if val == "N/A":
            return "N/A"
    vals.sort()

    vmap = {}
    for i in range(0, 3):
        vmap[vals[i+2]-vals[i]] = [vals[i], vals[i+1], vals[i+2]]

    return sum(vmap[min(vmap)])/3.0


def AvgTestResultTable(tabs):
    assert len(tabs) == 5
    for (i, j) in ((i, j) for i in range(5) for j in range(5) if i != j):
        assert tabs[i].Compatible(tabs[j])

    res = copy.deepcopy(tabs[0])
    for (i, rows) in enumerate(zip(*[tab.data for tab in tabs])):
        for (col, header) in enumerate(res.headers):
            if header.dataType == ColumnDataType.Number:
                vals = [row[col] for row in rows]
                res.data[i][col] = AvgVal(vals)

    return res


def AvgTestResult(results):

    result_num = len(results)
    for (i, j) in ((i, j) for i in range(result_num) for j in range(result_num)):
        assert results[i].Compatible(results[j])

    res = TestResult()
    for tabs in zip(*[result.tabs for result in results]):
        res.tabs.append(AvgTestResultTable(tabs))

    assert res.Compatible(results[0])

    return res


def CmpTestResultTable(lhs, rhs):
    pass


def CmpTestResult(lhs, rhs):
    pass


if __name__ == "__main__":
    pass
