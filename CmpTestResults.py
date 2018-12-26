# coding=utf-8

from TestResults import TestResult, AvgTestResult, CmpTestResult

TEST_RESULT_FILE = r"data\shaderbench\Ariel_llpc\{}\001\test_results.txt"
AVG_TEST_RESULT_FILE = r"data\shaderbench\Ariel_llpc\avg_test_results.txt"
CMP_TEST_RESULT_FILE = r"data\shaderbench\Ariel_llpc\cmp_test_results.txt"

rs = []
for i in range(1, 6):
    testResult = TestResult(TEST_RESULT_FILE.format(i))
    testResult.LoadData()
    rs.append(testResult)

avgResult = AvgTestResult(rs)
with open(AVG_TEST_RESULT_FILE, "w") as f:
    f.write(avgResult.ResultLines())

cmpResult = CmpTestResult(rs[0], avgResult)
with open(CMP_TEST_RESULT_FILE, "w") as f:
    f.write(cmpResult.ResultLines())
