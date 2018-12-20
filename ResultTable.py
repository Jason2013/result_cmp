# coding=utf-8

from enum import Enum
class RowState(Enum):
    Misc = 1
    ResultHeader = 2
    ResultData = 3
    ResultEnd = 4

TEST_RESULTS_FILE = r"D:\work\dev\teamcity\data\shaderbench\Ariel_llpc\1\001\test_results.txt"
