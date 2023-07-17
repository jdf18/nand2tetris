import sys
from enum import Enum
from typing import Union, TextIO

class CommandType(Enum):
	NONE = 0
	C_ARITHMETIC = 1
	C_PUSH       = 2
	C_POP        = 3
	C_LABEL      = 4
	C_GOTO       = 5
	C_IF         = 6
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

class Command:
	command_type: CommandType
	argument_1: Union[ArithmeticType, MemorySegment, None]
	argument_2: Union[int, None]

	def __init__(self) -> None:
		self.command_type = CommandType.NONE
		self.argument_1 = None
		self.argument_2 = None

	def __repr__(self) -> str:
		return self.string()
	def string(self) -> str:
		out =  f'<class Command\n    type: {self.command_type.name}\n'
		if self.argument_1 != None: out += f'    arg1: {self.argument_1}\n'
		if self.argument_2 != None: out += f'    arg2: {self.argument_2}\n'
		return str(out + '>')

class Parser:
	def __init__(self, file_stream: TextIO):
		self.file_stream = file_stream
	def __iter__(self):
		return self
	def __next__(self) -> Union[Command, StopIteration]:
		line = self.file_stream.readline()
		if line == '': raise StopIteration

		command: Command = self.parse(line)
		return command
	
	def parse(self, line: str):
		parts = line.split(' ')
		parts.extend(['','',''])
		parts = tuple(map(str.strip, parts))
		str_command_type, str_argument_1, str_argument_2, *_ = parts
		command = Command()

		#* Check for comment
		if line.strip()[:2] == '//' or parts[0] == '':
			return None


		#* Parse command
		if str_command_type in ('add','sub','neg','eq','gt','lt','and','or','not'):
			command.command_type = CommandType.C_ARITHMETIC
		elif str_command_type == 'push':
			command.command_type = CommandType.C_PUSH
		elif str_command_type == 'pop':
			command.command_type = CommandType.C_POP
		# elif str_command_type == 'label':
		# 	command.command_type = CommandType.C_LABEL
		# elif str_command_type == 'goto':
		# 	command.command_type = CommandType.C_GOTO
		# elif str_command_type == 'if':
		# 	command.command_type = CommandType.C_IF
		# elif str_command_type == 'function':
		# 	command.command_type = CommandType.C_FUNCTION
		# elif str_command_type == 'return':
		# 	command.command_type = CommandType.C_RETURN
		# elif str_command_type == 'call':
		# 	command.command_type = CommandType.C_CALL
		

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

			command.argument_2 = int(str_argument_2)

		return command

class CodeWriter:
	def __init__(self, output_stream: TextIO, memory_map: MemoryMap = MemoryMap()):
		self.output_stream = output_stream
		self.map = memory_map
	def writeCommand(self, command: Command, index: int) -> int:
		output = '\n\n'
		if command.command_type == CommandType.C_ARITHMETIC:
			if command.argument_1 in (ArithmeticType.A_NEGATE, ArithmeticType.A_NOT):
				#* Decrement the stack pointer
				output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

				if command.argument_1 == ArithmeticType.A_NEGATE:
					output += 'M = -M\n'
				elif command.argument_1 == ArithmeticType.A_NOT:
					output += 'M = !M\n'

				#* Increment the stack pointer
				output += '@SP\nM = M+1\n' # Increment the Stack Pointer
			elif command.argument_1 in (ArithmeticType.A_EQUALS, ArithmeticType.A_GREATER, ArithmeticType.A_LESS):
				#* Decrement the stack pointer
				output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

				#* Get the item on the top of the stack and store in D
				output += 'D = M\n'               # Store the stack value into the D register

				#* Decrement the stack pointer
				output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

				#* Perform the calculation
				if command.argument_1 == ArithmeticType.A_EQUALS:
					output += 'D = M-D\n'
					output += '@SP\nA = M\nM = -1\n' # set M to true
					index += len([i for i in output.splitlines() if i])
					output += f'@{str(index + 5)}\n' # set jump location
					output += 'D; JEQ\n' # if is equal then skip set M to false
					output += '@SP\nA = M\nM = 0\n' # set M to false
				elif command.argument_1 == ArithmeticType.A_GREATER:
					output += 'D = M-D\n'
					output += '@SP\nA = M\nM = -1\n' # set M to true
					index += len([i for i in output.splitlines() if i])
					output += f'@{str(index + 5)}\n' # set jump location
					output += 'D; JGT\n' # if is greater then skip set M to false
					output += '@SP\nA = M\nM = 0\n' # set M to false
				elif command.argument_1 == ArithmeticType.A_LESS:
					output += 'D = M-D\n'
					output += '@SP\nA = M\nM = -1\n' # set M to true
					index += len([i for i in output.splitlines() if i])
					output += f'@{str(index + 5)}\n' # set jump location
					output += 'D; JLT\n' # if is less then skip set M to false
					output += '@SP\nA = M\nM = 0\n' # set M to false

				
				#* Increment the stack pointer
				output += '@SP\nM = M+1\n' # Increment the Stack Pointer
			else:
				#* Decrement the stack pointer
				output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

				#* Get the item on the top of the stack and store in D
				output += 'D = M\n'               # Store the stack value into the D register

				#* Decrement the stack pointer
				output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

				#* Perform the calculation
				if command.argument_1 == ArithmeticType.A_ADD:
					output += 'D = D+M\n'
				elif command.argument_1 == ArithmeticType.A_SUBTRACT:
					output += 'D = M-D\n'
				elif command.argument_1 == ArithmeticType.A_AND:
					output += 'D = D&M\n'
				elif command.argument_1 == ArithmeticType.A_OR:
					output += 'D = D|M\n'
				
				#* Store the output on the stack
				output += '@SP\nA = M\n'
				output += 'M = D\n'

				#* Increment the stack pointer
				output += '@SP\nM = M+1\n' # Increment the Stack Pointer
			
		elif command.command_type in (CommandType.C_PUSH, CommandType.C_POP):
			if command.command_type == CommandType.C_PUSH:
				#* D = Value to be pushed
				if command.argument_1 == MemorySegment.S_CONSTANT:
					output += f'@{str(command.argument_2)}\n' # Loads the constant value into the A register
					output += 'D = A\n'                       # Moves the constant from the A register into the D register
				elif command.argument_1 == MemorySegment.S_TEMP:
					output += f'@{str(5+int(command.argument_2))}\n'
					output += 'D = M\n'
				elif command.argument_1 == MemorySegment.S_POINTER:
					output += f'@{str(self.map.query(MemorySegment.S_POINTER, command.argument_2))}\n'
					output += 'D = M\n'
				else:
					output += f'@{str(self.map.query(command.argument_1))}\n' # Load the base address pointer into register A
					output += 'D = M\n'                                       # Get the base address and store it in D
					output += f'@{str(command.argument_2)}\n'                 # Load the offset into the A register
					output += 'A = D+A\n'                                     # Calculate the memory address
					output += 'D = M\n'                                       # Store the value into the D register

				#* Get the address of the top of the stack
				output += '@SP\n'          # Loads the address of the Stack Pointer into the A register
				output += 'A = M\n'        # Sets the address to the Stack Item

				#* Set the item on the top of the stack to D
				output += 'M = D\n'        # Sets the memory item to the data value

				#* Increment the stack pointer
				output += '@SP\nM = M+1\n' # Increment the Stack Pointer

			elif command.command_type == CommandType.C_POP:
				if command.argument_1 in (MemorySegment.S_TEMP, MemorySegment.S_POINTER):
					#* Decrement the stack pointer
					output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

					#* Get the item on the top of the stack and store in D
					output += 'D = M\n'               # Store the stack value into the D register
					
					#* Calculate the address to store the value in
					if command.argument_1 == MemorySegment.S_TEMP:
						output += f'@{str(5+int(command.argument_2))}\n'
					elif command.argument_1 == MemorySegment.S_POINTER:
						output += f'@{str(self.map.query(MemorySegment.S_POINTER, command.argument_2))}\n'

					#* Store the value held in D into the correct address in memory
					output += 'M = D\n'               # Store the value into memory
				else:
					#* Calculate the address to store the value in
					output += f'@{str(self.map.query(command.argument_1))}\n' # Load the base address pointer into register A
					output += 'D = M\n'                                        # Get the base address and store it in D
					output += f'@{str(command.argument_2)}\n'                  # Load the offset into the A register
					output += 'D = D+A\n'                                      # Calculate the memory address
					output += '@13\nM = D\n'                                   # Store the address in register 13

					#* Decrement the stack pointer
					output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

					#* Get the item on the top of the stack and store in D
					output += 'D = M\n'        # Store the stack value into the D register

					#* Store the value held in D into the correct address in memory
					output += '@13\nA = M\n'   # Fetch the address from the temporary variable
					output += 'M = D\n'        # Store the value into the memory
				
		# write the assembly to the file
		self.output_stream.write(output)

		# return the amount of instructions sent
		return len([i for i in output.splitlines() if i])

if __name__ == "__main__":
	filepath = sys.argv[1]
	read_file = open(filepath)
	write_file = open(filepath[:filepath.rindex('.')]+'.asm', 'w')

	parser = Parser(read_file)
	writer = CodeWriter(write_file)

	index = 0
	for command in parser:
		if command:
			no_commands = writer.writeCommand(command, index=index)
			index += no_commands
	
	read_file.close()
	write_file.close()
	