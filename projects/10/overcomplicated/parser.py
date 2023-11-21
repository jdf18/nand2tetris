from enum import Enum
from typing import Union, Tuple, Iterator, List, Any, Iterable, Dict
import re

# ! PUT INTO UTIL CLASS
class SmartIter:
    def __init__(self, iter: Iterable):
        self.values = tuple(iter)
        self.counter = 0
    def __next__(self):
        if self.counter == len(self.values):
            raise StopIteration()
        self.counter += 1
        return self.values[self.counter-1]
    def look_ahead(self, num):
        if self.counter + num >= len(self.values): return ' '
        else: return self.values[self.counter-1 + num]
    def reverse(self, num):
        self.counter -= num

class JackTokeniser:
    class Token:
        pass
    class Keywords(Enum):
        CLASS = 0
        METHOD = 1
        FUNCTION = 2
        CONSTRUCTOR = 3
        INT = 4
        BOOLEAN = 5
        CHAR = 6
        VOID = 7
        VAR = 8
        STATIC = 9
        FIELD = 10
        LET = 11
        DO = 12
        IF = 13
        ELSE = 14
        WHILE = 15
        RETURN = 16
        TRUE = 17
        FALSE = 18
        NULL = 19
        THIS = 20
    def __init__(self, text_stream):
        self.input_iter = SmartIter(text_stream)
        
class CompilationEnginge:
    pass

class JackAnalyser:
    pass