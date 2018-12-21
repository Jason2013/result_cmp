# coding=utf-8

from enum import Enum
class RowState(Enum):
    Misc = 1
    ResultHeader = 2
    ResultData = 3
    ResultEnd = 4

TEST_RESULTS_FILE = r"D:\work\dev\teamcity\data\shaderbench\Ariel_llpc\1\001\test_results.txt"


class TestResult(object):

    def __init__(self, TestResultFile = None):
        self.testResultFile = TestResultFile if TestResultFile else None

    def LoadData(self):
        state = RowState.Misc
        with open(self.testResultFile) as f:
            for row in (x.rstrip() for x in f):
                if state == RowState.Misc:
                    # if 
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
