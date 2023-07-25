from typing import Union, TextIO
from enum import Enum

from util import str_sum

class CommandType(Enum):
	NONE = 0
	C_ARITHMETIC = 1
	C_PUSH       = 2
	C_POP        = 3
	C_LABEL      = 4
	C_GOTO       = 5
	C_IFGOTO     = 6
	C_FUNCTION   = 7
	C_RETURN     = 8
	C_CALL       = 9

class ArithmeticType(Enum):
	NONE = 0
	A_ADD      = 1
	A_SUBTRACT = 2
	A_NEGATE   = 3
	A_EQUALS   = 4
	A_GREATER  = 5
	A_LESS     = 6
	A_AND      = 7
	A_OR       = 8
	A_NOT      = 9
	
class MemorySegment(Enum):
	NONE = 0
	S_LOCAL    = 1
	S_ARGUMENT = 2
	S_THIS     = 3
	S_THAT     = 4
	S_CONSTANT = 5
	S_STATIC   = 6
	S_TEMP     = 7
	S_POINTER  = 8

class Symbols(Enum):
	NONE = None
	SP   = 1
	LCL  = 2
	ARG  = 3
	THIS = 4
	THAT = 5
	R13  = 6
	R14  = 7
	R15  = 8
	# Xxx.i 

class MemoryMap:
	def __init__(self) -> None:
		self.stack_pointer = 0
		self.local_pointer = 1
		self.argument_pointer = 2
		self.this_pointer = 3
		self.that_pointer = 4
	def query(self, segment: MemorySegment, arg=None) -> int:
		if segment == MemorySegment.S_LOCAL:
			return self.local_pointer
		elif segment == MemorySegment.S_ARGUMENT:
			return self.argument_pointer
		elif segment == MemorySegment.S_THIS:
			return self.this_pointer
		elif segment == MemorySegment.S_THAT:
			return self.that_pointer
		elif segment == MemorySegment.S_POINTER:
			if arg == 0:
				return self.this_pointer
			elif arg == 1:
				return self.that_pointer
			else:
				raise Exception("Invalid pointer segment")

class VMCommand:
	command_type: CommandType
	argument_1: Union[ArithmeticType, MemorySegment, str, None]
	argument_2: Union[int, None]

	def __init__(self) -> None:
		self.command_type = CommandType.NONE
		self.argument_1 = None
		self.argument_2 = None

	def __repr__(self) -> str:
		return self.string()
	
	def string(self) -> str:
		out =  '<class Command: type={:<12}, '.format(self.command_type.name)
		if self.argument_1 != None: out += 'arg1={:<10}, '.format(
				(self.argument_1 if type(self.argument_1) == str else self.argument_1.name)
			)
		if self.argument_2 != None: out += 'arg2={:<4}, '.format(self.argument_2)

		return str(out[:-2] + '>')


class VMProgram:
	class VMClass:
		class VMFunction:
			def __init__(self, name: str, n_local_vars: int) -> None:
				self.name = name
				self.n_local_vars = n_local_vars
				self.instructions: list[VMCommand] = []

			def __repr__(self) -> str:
				return self.name

		def __init__(self, name:str) -> None:
			self.name = name
			self.functions: list[VMProgram.VMClass.VMFunction] = []
		def add_function(self, function: VMFunction):
			self.functions.append(function)
		def __repr__(self) -> str:
			return f"<{self.name}" + str_sum(['  ' + i.__repr__() for i in self.functions]) + '>'

	def __init__(self) -> None:
		self.classes: list[VMProgram.VMClass] = []

	def __repr__(self) -> str:
		return "<VMProgram\n" + str_sum(['\t'+cls.__repr__()+'\n' for cls in self.classes]) + '>'
	def load_text(self, class_name: str, text: str):
		new_class = self.VMClass(class_name)

		parser = Parser(text)
		commands: list[VMCommand] = []
		current_function: VMProgram.VMClass.VMFunction = None
		for command in parser:
			if command.command_type == CommandType.C_FUNCTION:
				current_function = VMProgram.VMClass.VMFunction(command.argument_1, command.argument_2)
			commands.append(command)
			if command.command_type == CommandType.C_RETURN:
				current_function.instructions = commands
				new_class.add_function(current_function)
				commands = []

		self.classes.append(new_class)
			

class Parser:
	def __init__(self, text: str):
		self.text = text
		self.lines = self.text.splitlines()
		
		self.remove_comments()

	def remove_comments(self):
		#* Remove comments or blank lines
		self.lines = list(filter(
			lambda line : not (line.strip()[:2] == '//' or line.strip() == ''),
			self.lines
		))
		for line in self.lines:
			index = line.find('//')
			if index == -1: continue
			
			line = line[:index]

	def __iter__(self):
		return self
	def __next__(self) -> Union[VMCommand, StopIteration]:
		if len(self.lines) == 0: raise StopIteration

		line = self.lines.pop(0)
		
		command: VMCommand = self.parse(line)
		return command
	
	def parse(self, line: str):
		#* Split command
		parts = line.strip().split(' ')
		parts = tuple(map(str.strip, parts))
		if len(parts) == 1: str_command_type = parts[0]
		elif len(parts) == 2: str_command_type, str_argument_1 = parts
		elif len(parts) == 3: str_command_type, str_argument_1, str_argument_2 = parts

		command = VMCommand()

		#* Parse command
		if str_command_type in ('add','sub','neg','eq','gt','lt','and','or','not'):
			command.command_type = CommandType.C_ARITHMETIC
		elif str_command_type == 'push':
			command.command_type = CommandType.C_PUSH
		elif str_command_type == 'pop':
			command.command_type = CommandType.C_POP
		elif str_command_type == 'label':
			command.command_type = CommandType.C_LABEL
			command.argument_1 = str_argument_1
		elif str_command_type == 'goto':
			command.command_type = CommandType.C_GOTO
			command.argument_1 = str_argument_1
		elif str_command_type == 'if-goto':
			command.command_type = CommandType.C_IFGOTO
			command.argument_1 = str_argument_1
		elif str_command_type == 'function':
			command.command_type = CommandType.C_FUNCTION
			command.argument_1 = str_argument_1
			command.argument_2 = int(str_argument_2)
		elif str_command_type == 'return':
			command.command_type = CommandType.C_RETURN
		elif str_command_type == 'call':
			command.command_type = CommandType.C_CALL
			command.argument_1 = str_argument_1
			command.argument_2 = int(str_argument_2)
		

		if command.command_type == CommandType.C_ARITHMETIC:
			if str_command_type == 'add':
				command.argument_1 = ArithmeticType.A_ADD
			elif str_command_type == 'sub':
				command.argument_1 = ArithmeticType.A_SUBTRACT
			elif str_command_type == 'neg':
				command.argument_1 = ArithmeticType.A_NEGATE
			elif str_command_type == 'eq':
				command.argument_1 = ArithmeticType.A_EQUALS
			elif str_command_type == 'gt':
				command.argument_1 = ArithmeticType.A_GREATER
			elif str_command_type == 'lt':
				command.argument_1 = ArithmeticType.A_LESS
			elif str_command_type == 'and':
				command.argument_1 = ArithmeticType.A_AND
			elif str_command_type == 'or':
				command.argument_1 = ArithmeticType.A_OR
			elif str_command_type == 'not':
				command.argument_1 = ArithmeticType.A_NOT

			command.argument_2 = None
		elif command.command_type in (CommandType.C_PUSH, CommandType.C_POP):
			if str_argument_1 == 'local':
				command.argument_1 = MemorySegment.S_LOCAL
			elif str_argument_1 == 'argument':
				command.argument_1 = MemorySegment.S_ARGUMENT
			elif str_argument_1 == 'this':
				command.argument_1 = MemorySegment.S_THIS
			elif str_argument_1 == 'that':
				command.argument_1 = MemorySegment.S_THAT
			elif str_argument_1 == 'constant':
				command.argument_1 = MemorySegment.S_CONSTANT
			elif str_argument_1 == 'static':
				command.argument_1 = MemorySegment.S_STATIC
			elif str_argument_1 == 'temp':
				command.argument_1 = MemorySegment.S_TEMP
			elif str_argument_1 == 'pointer':
				command.argument_1 = MemorySegment.S_POINTER

			command.argument_2 = int(str_argument_2.rstrip())

		return command
	
	def close(self):
		self.file_stream.close()
		return
	
if __name__ == '__main__':
	with open('..\\08\\FunctionCalls\\StaticsTest\\Class1.vm') as file:
		content = file.read()

	x = VMProgram()
	x.load_text('Class1', content)

	print(x)