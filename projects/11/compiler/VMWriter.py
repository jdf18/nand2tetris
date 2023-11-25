from enum import Enum

class SEGMENT(Enum):
    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

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
    def __init__(self, classname):
        self.vm_code = ''
        self.classname = classname
    def write_push(self, segment: SEGMENT, index: int):
        # Writes a VM PUSH command
        self.vm_code += f"    push {segment.value.lower()} {str(index)}\n"
    def write_pop(self, segment: SEGMENT, index: int):
        # Writes a VM POP command
        assert segment != SEGMENT.CONST
        self.vm_code += f"    pop {segment.value.lower()} {str(index)}\n"
    def write_arithmetic(self, command: COMMAND):
        # Writes a VM arithmetic-logical command
        self.vm_code += f"    {command.name.lower()}\n"
    def write_label(self, label: str):
        # Writes a VM label command
        self.vm_code += f"label {label}\n"
    def write_goto(self, label: str):
        # Writes a VM goto command
        self.vm_code += f"    goto {label}\n"
    def write_if(self, label: str):
        # Writes a VM if-goto command
        self.vm_code += f"    if-goto {label}\n"
    def write_call(self, label: str, n_args: int):
        # Writes a VM call command
        self.vm_code += f"    call {label} {str(n_args)}\n"
    def write_function(self, label: str, n_locals: int):
        # Writes a VM function command
        self.vm_code += f"function {self.classname}.{label} {str(n_locals)}\n"
    def write_return(self):
        # Writes a VM return command
        self.vm_code += "    return\n"