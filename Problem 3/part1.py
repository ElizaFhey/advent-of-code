import numpy as np
import dataclasses
import string
from typing import List, Tuple

@dataclasses.dataclass
class Point:
    x : int
    y : int

@dataclasses.dataclass
class Location:
    position : Point
    size : Point

    @property
    def left(self):
        return self.position.x
    
    @property
    def right(self):
        return self.position.x + self.size.x
    
    @property
    def top(self):
        return self.position.y
    
    @property
    def bottom(self):
        return self.position.y + self.size.y

    def contains(self, pos : Point):
        return pos.x >= self.left and pos.x < self.right and pos.y >= self.top and pos.y < self.bottom
    
    def touches(self, pos : Point):
        between_horz = self.left - 1 <= pos.x and pos.x <= self.right
        between_vert = self.top - 1 <= pos.y and pos.y <= self.bottom
        return between_horz and between_vert
        #return (((self.left - pos.x) == 1 or (pos.x - self.right) == 0) and between_vert) or (((self.top - pos.y) == 1 or (pos.y - self.bottom) == 0) and between_horz)

@dataclasses.dataclass
class NumberBlock:
    value : str
    location : Location

    def __int__(self):
        return int(self.value)
    
@dataclasses.dataclass
class Symbol:
    value : str
    location : Point
    
numbers : List[NumberBlock] = []
symbols : List[Symbol] = []

with open('Problem 3/input.txt', 'r') as f:
    for ln, line in enumerate(f.readlines()):
        num = None
        for p, ch in enumerate(line.strip()):
            if '.' == ch:
                if  num is not None:
                    numbers.append(num)
                num = None
            elif ch in string.digits:
                if num is not None:
                    num.value += ch
                    num.location.size.x += 1
                else:
                    num = NumberBlock(ch, Location(Point(p, ln), Point(1, 1)))
            else:
                if num is not None:
                    numbers.append(num)
                    num = None
                symbols.append(Symbol(ch, Point(p, ln)))
        if num is not None:
            numbers.append(num)

touching_nums = []
for num in numbers:
    for sym in symbols:
        if num.location.touches(sym.location):
            #print(f'{num} touches {sym}')
            touching_nums.append(num)
            break
    # else:
    #     print(f"{num} didn't touch anything")

#print("Found touching numbers:")
# for x in touching_nums:
#     print(x)

result = sum(int(x) for x in touching_nums)
print(f'Found result: {result}')