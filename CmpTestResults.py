# coding=utf-8

import sys
from TestResults import TestResult, AvgTestResult, CmpTestResult

def RunAvgTestResult(files):
    print(files)
    rs = []
    for i in range(0, 5):
        testResult = TestResult(files[i])
        testResult.LoadData()
        rs.append(testResult)

    avgResult = AvgTestResult(rs)
    with open(files[5], "w") as f:
        f.write(avgResult.ResultLines())

def RunCmpTestResult(files):
    rs = []
    for i in range(0, 2):
        testResult = TestResult(files[i])
        testResult.LoadData()
        rs.append(testResult)

    cmpResult = CmpTestResult(rs[0], rs[1])
    with open(files[2], "w") as f:
        f.write(cmpResult.ResultLines())

if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else None
    if option == "-a":
        RunAvgTestResult(sys.argv[2:8])
    elif option == "-c":
        RunCmpTestResult(sys.argv[2:5])
    else:
        print("""Usage:
  {SCRIPT} -a INPUT1 INPUT2 INPUT3 INPUT4 INPUT5 OUTPUT
  {SCRIPT} -c INPUT1 INPUT2 OUTPUT
""".format(SCRIPT=sys.argv[0]))
