'''
Created on Oct 3, 2024

@author: acre
'''
import unittest
import corn
from typing import List


def read(file: str) -> List[List[int]]:
    with open(file, "r") as f:
        field: List[List[int]] = f.read()
    field = [[int(x) for x in y] for y in field.strip().split('\n')]
    return field


class Test(unittest.TestCase):
    
    def _testHelper(self, field, expectedVisibleCount : int, expectedEliteMax : int) -> bool:
        field = corn.Field(field)
        visible = corn.Visible(field)
        scorer = corn.VisibilityScorer(field)
        self.assertEqual(visible.count(), expectedVisibleCount)
        self.assertEqual(scorer.findEliteMax(), expectedEliteMax)
        return True
        
    def test1(self):
        field = [
            [4, 1, 4, 8, 4],
            [3, 6, 6, 2, 3],
            [7, 6, 4, 4, 3],
            [4, 4, 6, 5, 0],
            [4, 6, 4, 0, 1]
        ]
        self._testHelper(field, 22, 8)

    def test2(self):
        field = [
            [4, 1, 4, 8, 4],
            [3, 6, 6, 2, 3],
            [7, 6, 4, 4, 3],
            [4, 4, 6, 5, 0],
            [4, 6, 4, 0, 1],
            [4, 7, 3, 0, 1]
        ]
        self._testHelper(field, 26, 16)

    # isolated valley: the 4 is surrounded by 6
    def test3(self):
        field = [
            [4, 1, 4, 8, 4],
            [3, 6, 6, 6, 3],
            [7, 6, 4, 6, 3],
            [4, 6, 6, 6, 0],
            [4, 6, 4, 0, 1]
        ]
        self._testHelper(field, 23, 2)
    
    # middle plateau of 6s
    def test4(self):
        field = [
            [4, 1, 4, 8, 4],
            [3, 6, 6, 6, 3],
            [7, 6, 6, 6, 3],
            [4, 6, 6, 6, 0],
            [4, 6, 4, 0, 1]
        ]
        self._testHelper(field, 23, 1)

    # provided test case
    def test5(self):
        self._testHelper(read("input.txt"), 1700, 470596)

    # 1 on boundary, 0 inside
    def test6(self):
        field = [[1] * 100] + [[1] + [0]*98 + [1]]*98 + [[1]*100]
        self._testHelper(field, 396, 1)

    # long pyramid slope
    def test7(self):
        field = []
        for x in range(1000):
            field.append([x + z for z in range(1000)])
            
        self._testHelper(field, 1000000, 996004)
    
    # edge case
    def test8(self):
        field = [
            [1]
        ]
        self._testHelper(field, 1, 0)
        
    # edge case
    def test9(self):
        field = [
            [1, 1]
        ]
        self._testHelper(field, 2, 0)
        
    # edge case
    def test10(self):
        field = [
            [1, 1],
            [1, 1]
        ]
        self._testHelper(field, 4, 0)
        
    # edge case
    def test11(self):
        field = [
            [1, 1, 1],
            [1, 1, 1]
        ]
        self._testHelper(field, 6, 0)
        
    # edge case
    def test12(self):
        field = [
            [1, 7, 1],
            [2, 9, 5],
            [1, 3, 1]
        ]
        self._testHelper(field, 9, 1)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
