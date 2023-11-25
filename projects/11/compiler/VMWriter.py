from enum import Enum

class SEGMENT(Enum):
    CONST = 0
    ARG = 1
    LOCAL = 2
    STATIC = 3 
    THIS = 4
    THAT = 5
    POINTER = 6
    TEMP = 7

class COMMAND(Enum):
    ADD = 0
    SUB = 1
    NEG = 2
    EQ  = 3
    GT  = 4
    LT  = 5
    AND = 6
    OR  = 7
    NOT = 8

class VMWriter:
    def __init__(self):
        self.vm_code = ''
    def write_push(self, segment: SEGMENT, index: int):
        # Writes a VM PUSH command
        pass
    def write_pop(self, segment: SEGMENT, index: int):
        # Writes a VM POP command
        assert segment != SEGMENT.CONST
        pass
    def write_arithmetic(self, command: COMMAND):
        # Writes a VM arithmetic-logical command
        pass
    def write_label(self, label: str):
        # Writes a VM label command
        pass
    def write_goto(self, label: str):
        # Writes a VM goto command
        pass
    def write_if(self, label: str):
        # Writes a VM if-goto command
        pass
    def write_call(self, label: str, n_args: int):
        # Writes a VM call command
        pass
    def write_function(self, label: str, n_locals: int):
        # Writes a VM function command
        pass
    def write_return(self):
        # Writes a VM return command
        pass