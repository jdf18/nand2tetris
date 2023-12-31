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

SEGMENT_LUT = {
    SEGMENT.CONST : "constant",
    SEGMENT.ARG : "argument",
    SEGMENT.LOCAL : "local",
    SEGMENT.STATIC : "static",
    SEGMENT.THIS : "this",
    SEGMENT.THAT : "that",
    SEGMENT.POINTER : "pointer",
    SEGMENT.TEMP : "temp"
}

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

indent = ""
#indent = "    "

class VMWriter:
    def __init__(self, classname):
        self.vm_code = ''
        self.classname = classname
    def write_push(self, segment: SEGMENT, index: int):
        # Writes a VM PUSH command
        self.vm_code += f"{indent}push {SEGMENT_LUT[segment]} {str(index)}\n"
    def write_pop(self, segment: SEGMENT, index: int):
        # Writes a VM POP command
        assert segment != SEGMENT.CONST
        self.vm_code += f"{indent}pop {SEGMENT_LUT[segment]} {str(index)}\n"
    def write_arithmetic(self, command: COMMAND):
        # Writes a VM arithmetic-logical command
        self.vm_code += f"{indent}{command.name.lower()}\n"
    def write_label(self, label: str):
        # Writes a VM label command
        self.vm_code += f"label {label}\n"
    def write_goto(self, label: str):
        # Writes a VM goto command
        self.vm_code += f"{indent}goto {label}\n"
    def write_if(self, label: str):
        # Writes a VM if-goto command
        self.vm_code += f"{indent}if-goto {label}\n"
    def write_call(self, label: str, n_args: int):
        # Writes a VM call command
        self.vm_code += f"{indent}call {label} {str(n_args)}\n"
    def write_function(self, label: str, n_locals: int):
        # Writes a VM function command
        self.vm_code += f"function {self.classname}.{label} {str(n_locals)}\n"
    def write_return(self):
        # Writes a VM return command
        self.vm_code += f"{indent}return\n"