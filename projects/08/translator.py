import sys, os
import argparse
from enum import Enum
from typing import Union, TextIO
import uuid

def get_rand_str() -> str:
	return uuid.uuid4().hex[:8]

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

class Command:
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
		#* Check for comment or blank line
		
		parts = line.strip().split(' ')
		parts.extend(['','',''])
		parts = tuple(map(str.strip, parts))

		if line.strip()[:2] == '//':
			return None
		elif line.strip().find('//') != -1:
			line = line.strip()[:line.strip().index('//')]
		elif parts[0] == '':
			return None
		
		parts = line.strip().split(' ')
		parts.extend(['','',''])
		parts = tuple(map(str.strip, parts))
		str_command_type, str_argument_1, str_argument_2, *_ = parts
		command = Command()

		


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

class CodeWriter:
	def __init__(self, output_stream: TextIO, memory_map: MemoryMap = MemoryMap()):
		self.output_stream = output_stream
		self.map = memory_map
		self.current_file = None
		self.current_static_base = 16
		self.next_static_alloc = 16
	def writeCommand(self, command: Command, index: int) -> int:
		output = '\n'
		
		if command.command_type == CommandType.C_ARITHMETIC:
			output = self.writeArithmetic(command, index)
		elif command.command_type in (CommandType.C_PUSH, CommandType.C_POP):
			output = self.writePushPop(command, index)
		elif command.command_type == CommandType.C_LABEL:
			output = self.writeLabel(command, index)
		elif command.command_type == CommandType.C_GOTO:
			output = self.writeGoto(command, index)
		elif command.command_type == CommandType.C_IFGOTO:
			output = self.writeIf(command, index)
		elif command.command_type == CommandType.C_FUNCTION:
			output = self.writeFunction(command, index)
		elif command.command_type == CommandType.C_CALL:
			output = self.writeCall(command, index)
		elif command.command_type == CommandType.C_RETURN:
			output = self.writeReturn(command, index)

		# write the assembly to the file
		self.output_stream.write(output)

		# return the amount of instructions sent
		return len([i for i in output.splitlines() if i])
	
	def close(self):
		#* Closes the output file
		self.output_stream.close()
		return
	
	def writeArithmetic(self, command: Command, index: int) -> int:
		#* Writes to the output file the assembly code that implements
		#* the given arithmetic command
		output = '\n'
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
			branch_id = get_rand_str()
			if command.argument_1 == ArithmeticType.A_EQUALS:
				output += 'D = M-D\n'
				output += '@SP\nA = M\nM = -1\n' # set M to true
				output += f'@{branch_id}\n' # set jump location
				output += 'D; JEQ\n' # if is equal then skip set M to false
				output += '@SP\nA = M\nM = 0\n' # set M to false
				output += f'({branch_id})\n'
			elif command.argument_1 == ArithmeticType.A_GREATER:
				output += 'D = M-D\n'
				output += '@SP\nA = M\nM = -1\n' # set M to true
				output += f'@{branch_id}\n' # set jump location
				output += 'D; JGT\n' # if is greater then skip set M to false
				output += '@SP\nA = M\nM = 0\n' # set M to false
				output += f'({branch_id})\n'
			elif command.argument_1 == ArithmeticType.A_LESS:
				output += 'D = M-D\n'
				output += '@SP\nA = M\nM = -1\n' # set M to true
				output += f'@{branch_id}\n' # set jump location
				output += 'D; JLT\n' # if is less then skip set M to false
				output += '@SP\nA = M\nM = 0\n' # set M to false
				output += f'({branch_id})\n'

			
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
		return output
	
	def writePushPop(self, command: Command, index: int) -> str:
		#* Writes to the output file the assembly code that implements
		#* the given command, where the command is either C_PUSH or C_POP
		output = '\n'
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
			elif command.argument_1 == MemorySegment.S_STATIC:
				output += f'@{str(self.current_static_base + command.argument_2)}\n' # Load the base address pointer into register A
				output += 'D = M\n'                                                  # Store the value into the D register
				# If pushing to a static variable, update the next_static_alloc value
				if self.current_static_base + command.argument_2 >= self.next_static_alloc:
					self.next_static_alloc = self.current_static_base + command.argument_2 + 1
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
			if command.argument_1 in (MemorySegment.S_TEMP, MemorySegment.S_POINTER, MemorySegment.S_STATIC):
				#* Decrement the stack pointer
				output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

				#* Get the item on the top of the stack and store in D
				output += 'D = M\n'               # Store the stack value into the D register
				
				#* Calculate the address to store the value in
				if command.argument_1 == MemorySegment.S_TEMP:
					output += f'@{str(5+int(command.argument_2))}\n'
				elif command.argument_1 == MemorySegment.S_POINTER:
					output += f'@{str(self.map.query(MemorySegment.S_POINTER, command.argument_2))}\n'
				elif command.argument_1 == MemorySegment.S_STATIC:
					output += f'@{str(self.current_static_base + command.argument_2)}\n'

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
		return output
		
	def setFileName(self, filename: str):
		#* Informs the CodeWriter that the translation of a new VM file has
		#* started (called by the main program)
		self.current_file = filename
		self.current_static_base = self.next_static_alloc

	def writeInit(self) -> int:
		#* Writes the assembly instructions that effect the bootstrap code
		#* that ititializes the VM. This code must be placed at the beginning
		#* of the generated *.asm file.
		output = '@256\nD = A\n@SP\nM = D\n'
		command = Command()
		command.command_type = CommandType.C_CALL
		command.argument_1   = 'Sys.init'
		command.argument_2   = 0
		output += self.writeCall(command, 4)

		self.output_stream.write(output)

		# return the amount of instructions sent
		return len([i for i in output.splitlines() if i])

	def writeLabel(self, command: Command, index: int) -> str:
		#* Writes assembly code that effects the label command
		output = '\n'
		output += f'({command.argument_1})'
		return output

	def writeGoto(self, command: Command, index: int) -> str:
		#* Writes assembly code that effects the goto command
		output = '\n'
		output += f'@{command.argument_1}\n0; JEQ\n'
		return output

	def writeIf(self, command: Command, index: int) -> str:
		#* Writes assembly code that effects the if-goto command
		output = '\n'
		output += '@SP\nM = M - 1\nA = M\nD = M\n' # Pop the item off the stack
		output += f'@{command.argument_1}\nD; JNE\n'
		return output

	def writeFunction(self, command: Command, index: int) -> str:
		#* Writes assembly code that effects the function command
		output = '\n'
		function_name = command.argument_1
		n_vars = command.argument_2
		output += f'({function_name})\n' # Write the label so that other parts of
		                                 # the program can branch to it
		command_push_0 = '@SP\nA = M\nM = 0\n@SP\nM = M+1\n'
		output += (command_push_0 * n_vars) # Push n_vars 0s to the stack
		return output

	def writeCall(self, command: Command, index: int) -> str:
		#* Writes assembly code that effects the call command
		output = '\n'
		retAddr = get_rand_str()
		# push returnAddress
		output += f'@{retAddr}\nD = A\n'
		output += '@SP\nA = M\nM = D\n'
		output += '@SP\nM = M+1\n'
		# push LCL
		output += '@LCL\nD = M\n'
		output += '@SP\nA = M\nM = D\n' # Add to the stack
		output += '@SP\nM = M+1\n'      # Increment the SP
		# push ARG
		output += '@ARG\nD = M\n'
		output += '@SP\nA = M\nM = D\n' # Add to the stack
		output += '@SP\nM = M+1\n'      # Increment the SP
		# push THIS
		output += '@THIS\nD = M\n'
		output += '@SP\nA = M\nM = D\n' # Add to the stack
		output += '@SP\nM = M+1\n'      # Increment the SP
		# push THAT
		output += '@THAT\nD = M\n'
		output += '@SP\nA = M\nM = D\n' # Add to the stack
		output += '@SP\nM = M+1\n'      # Increment the SP
		# ARG = SP-5-nArgs
		output += f'@SP\nD = M\n@{5+command.argument_2}\nD = D-A\n'
		output += '@ARG\nM = D\n'
		# LCL = SP
		output += '@SP\nD = M\n'
		output += '@LCL\nM = D\n'
		# goto function
		output += f'@{command.argument_1}\n0; JEQ\n'
		# label returnAddress
		output += f'({retAddr})\n'
		return output

	def writeReturn(self, command: Command, index: int) -> str:
		#* Writes assembly code that effects the return command
		output = '\n'
		endframe = '14' # ! switch to use these addersses
		retAddr = '15'
		# endFrame (@14 T1?) = LCL
		output += '@LCL\nD = M\n' # Store *LCL into D
		output += '@14\nM = D\n'  # Store D in temp 1
		# retAddr (@15 T2?) = *(endFrame - 5)
		output += '@5\nA = D-A\nD = M\n' # Store *(endFrame - 5) in D
		output += '@15\nM = D\n'         # Store D in temp 2
		#.*ARG = pop()
		output += '@SP\nM = M-1\n' # Decrement the SP
		output += 'A = M\nD = M\n' # Store the top value of the stack into D
		output += '@ARG\nA=M\nM = D\n'  # Store the return value into ARG 0
		# SP = ARG + 1
		output += 'D = A+1\n'    # Calculate the new SP
		output += '@SP\nM = D\n' # Set the new SP
		# THAT = *(endframe-1)
		output += '@14\nA = M-1\n' # Set the new address
		output += 'D = M\n'        # Stores the new *THAT in D
		output += '@THAT\nM = D\n' # Stores D in *THAT
		# THIS = *(endframe-2)
		output += '@14\nD = M\n' # Get the endFrame address
		output += '@2\nA = D-A\n' # Set the new address
		output += 'D = M\n'        # Stores the new *THIS in D
		output += '@THIS\nM = D\n' # Stores D in *THIS
		# ARG = *(endframe-3)
		output += '@14\nD = M\n' # Get the endFrame address
		output += '@3\nA = D-A\n' # Set the new address
		output += 'D = M\n'        # Stores the new *ARG in D
		output += '@ARG\nM = D\n' # Stores D in *ARG
		# LCL = *(endframe-4)
		output += '@14\nD = M\n' # Get the endFrame address
		output += '@4\nA = D-A\n' # Set the new address
		output += 'D = M\n'        # Stores the new *LCL in D
		output += '@LCL\nM = D\n' # Stores D in *LCL
		# goto retAddr
		output += '@15\nA = M\n0; JEQ\n'
		return output

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog="VM Translator",
		description="Converts VM programs into HACK assembly code",
	)
	parser.add_argument('filepath')
	parser.add_argument('-d', '--directory', action="store_true")
	parser.add_argument('--nobootloader', action="store_true")

	args = parser.parse_args()

	filepath = args.filepath
	is_directory = args.directory
	add_bootloader = not args.nobootloader

	if not is_directory:
		read_file = open(filepath)
		write_file = open(filepath[:filepath.rindex('.')]+'.asm', 'w')

		parser = Parser(read_file)
		writer = CodeWriter(write_file)

		if add_bootloader:
			index = writer.writeInit()
		else:
			index = 0

		for command in parser:
			if command:
				no_commands = writer.writeCommand(command, index=index)
				index += no_commands
		
		parser.close()
		writer.close()
	
	else:
		all_files = []
		for (root, dirs, files) in os.walk(filepath):
			all_files.extend(files)
		files = filter(
			lambda x : x[-3:] == '.vm',
			all_files
		)

		write_file = open(os.path.join(
			filepath, 
			filepath[filepath[:-1].rindex('\\')+1:]) + '.asm', 'w'
		)

		writer = CodeWriter(write_file)

		#! Do not use index, use labels instead
		if add_bootloader:
			index = writer.writeInit()
		else:
			index = 0

		#* Loop through each file
		for file in files:
			read_file = open(os.path.join(filepath, file))

			writer.setFileName(read_file.name[:-2])

			#* Parse each line and write the corresponding code
			parser = Parser(read_file)
			for command in parser:
				if command:
					no_commands = writer.writeCommand(command, index=index)
					index += no_commands

			parser.close()

		writer.close()
	