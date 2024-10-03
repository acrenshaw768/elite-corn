'''
Created on Oct 3, 2024

@author: acre
'''
from typing import List
from enum import IntEnum

class Direction(IntEnum):
    LEFT = 0,
    RIGHT = 1,
    DOWN = 2,
    UP = 3
        
class Field:
    def __init__(self, corn: List[List[int]]):
        self.corn: List[List[int]] = corn
        self.width: int = len(corn[0])
        self.length: int = len(corn)
        
class Visible:
    def __init__(self, field):
        self.field = field
        
    def count(self) -> int:
        """count corn plants visible in the field from outside"""
        visible: List[List[bool]] = self.initializeVisible()
        counter: int = self.initializeCounter()
        corn : List[List[int]] = self.field.corn
        length : int = self.field.length
        width : int = self.field.width
        
        for row in range(1, length - 1):
            # ignore the boundary
            left = 1
            right = width - 2
            left_max : int = corn[row][left - 1]
            right_max : int = corn[row][right + 1]
            # left and right pointers meet at peak.
            while left <= right:
                while left <= right and left_max <= right_max:
                    height : int = corn[row][left]
                    if(height > left_max):
                        left_max = height
                        if not visible[row][left]:
                            counter += 1
                            visible[row][left] = True
                    left += 1
                while left <= right and right_max <= left_max:
                    height : int = corn[row][right]
                    if(height > right_max):
                        right_max = height
                        if not visible[row][right]:
                            counter += 1
                            visible[row][right] = True
                    right += -1

        # same loop as above but rotate orientation.
        for row in range(width):
            left = 1
            right = length - 2
            left_max : int = corn[left - 1][row]
            right_max : int = corn[right + 1][row]
            while left <= right:
                while left <= right and left_max <= right_max:
                    height : int = corn[left][row]
                    if(height > left_max):
                        left_max = height
                        if not visible[left][row]:
                            counter += 1
                            visible[left][row] = True
                    left += 1
                while left <= right and right_max <= left_max:
                    height : int = corn[right][row]
                    if(height > right_max):
                        right_max = height
                        if not visible[right][row]:
                            counter += 1
                            visible[right][row] = True
                    right += -1
        return counter
    
    def initializeVisible(self) -> List[List[bool]]:
        """initialize with boundary conditions"""
        length : int = self.field.length
        width : int = self.field.width
        if length > 2 and width > 2: 
            return [[True] * width]\
                 + [[True] + ([False] * (width - 2)) + [True] for x in range(length - 2)]\
                 + [[True] * width]
        else:
            return [[True for x in range(width)] for y in range(length)]
    
    def initializeCounter(self) -> int:
        """initialize with boundary conditions"""
        length : int = self.field.length
        width : int = self.field.width
        if width == 1:
            return length
        elif length == 1:
            return width
        else:
            return (2 * width + 2 * length) - 4
        
class VisibilityScorer:
    def __init__(self, field):
        self.field = field
        
    def findEliteMax(self) -> int:
        """find the corn plant with the most visibility and return that visibility"""
        # the memory will store how far each corn can see in each direction.
        # 4 x Length x Width
        mem : List[List[List[int]]] = self.noneList()
        maxScore : int = 0
        
        # the boundary is always zero because it is a product.
        for y in range(1, self.field.length - 1):
            for x in range(1, self.field.width - 1):
                score : int = self.lookLeft(x, y, mem[Direction.LEFT])
                score = score * self.lookRight(x, y, mem[Direction.RIGHT])
                score = score * self.lookDown(x, y, mem[Direction.DOWN])
                score = score * self.lookUp(x, y, mem[Direction.UP])
                if(score > maxScore):
                    maxScore = score
        return maxScore

    def noneList(self) -> List[List[None]]:
        """initialize list for memory"""
        return [
            [
                [
                    None 
                    for x in range(self.field.width)
                ] 
                for y in range(self.field.length)
            ] 
            for z in range(len(Direction))
        ]
        
    def lookLeft(self, x: int, y : int, mem : List[List[int]]) -> int:
        """find how many corn plants can be seen from the left of (x, y)"""
        # check already visited
        if mem[y][x]:
            return mem[y][x]
        height : int = self.field.corn[y][x]
        shift = 1
        # shift left until reach a taller corn or boundary
        while x - shift > 0:
            if(self.field.corn[y][x - shift] >= height):
                # reached a taller corn. cannot see further. 
                mem[y][x] = shift
                return shift
            else:
                # this plant at (x, y) is taller than its neighbor at (x - shift, y) 
                # it can see whatever its neighbor can see. 
                # go to where the neighbor can see.
                shift += self.lookLeft(x - shift, y, mem)
        # reached the left boundary
        mem[y][x] = shift
        return shift

    def lookRight(self, x: int, y : int, mem : List[List[int]]) -> int:
        """find how many corn plants can be seen from the right of (x, y)"""
        # check already visited
        if mem[y][x]:
            return mem[y][x]
        height : int = self.field.corn[y][x]
        shift = 1
        # shift right until reach a taller corn or boundary
        while x + shift < self.field.width - 1:
            if(self.field.corn[y][x + shift] >= height):
                # reached a taller corn. cannot see further.
                mem[y][x] = shift
                return shift
            else:
                # this plant at (x, y) is taller than its neighbor at (x + shift, y) 
                # it can see whatever its neighbor can see. 
                # go to where the neighbor can see.
                shift += self.lookRight(x + shift, y, mem)
        mem[y][x] = shift
        return shift

    def lookDown(self, x: int, y : int, mem : List[List[int]]) -> int:
        """find how many corn plants can be seen down from (x, y)"""
        # check already visited
        if mem[y][x]:
            return mem[y][x]
        height : int = self.field.corn[y][x]
        shift = 1
        # shift down until reach a taller corn or boundary
        while y + shift < self.field.length - 1:
            if(self.field.corn[y + shift][x] >= height):
                # reached a taller corn. cannot see further. 
                mem[y][x] = shift
                return shift
            else:
                # this plant at (x, y) is taller than its neighbor at (x, y + shift) 
                # it can see whatever its neighbor can see. 
                # go to where the neighbor can see.
                shift += self.lookDown(x, y + shift, mem)
        mem[y][x] = shift
        return shift

    def lookUp(self, x: int, y : int, mem : List[List[int]]) -> int:
        """find how many corn plants can be seen up from (x, y)"""
        # check already visited
        if mem[y][x]:
            return mem[y][x]
        height : int = self.field.corn[y][x]
        shift = 1
        # shift up until reach a taller corn or boundary
        while y - shift > 0:
            if(self.field.corn[y - shift][x] >= height):
                # reached a taller corn. cannot see further. 
                mem[y][x] = shift
                return shift
            else:
                # this plant at (x, y) is taller than its neighbor at (x, y - shift) 
                # it can see whatever its neighbor can see. 
                # go to where the neighbor can see.
                shift += self.lookUp(x, y - shift, mem)
        mem[y][x] = shift
        return shift
    
    
    
