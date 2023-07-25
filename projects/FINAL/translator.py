import sys, os
import argparse
from enum import Enum
from typing import Union, TextIO

import VirtualMachine

#! Replace this as its stupid
import uuid
def get_rand_str() -> str:
	return uuid.uuid4().hex[:8]

class AssemblyProgram:
	class AssemblyInstruction:
		def __init__(self, instruction: str, label: str = None):
			self.instruction = instruction
			self.label = label

	def __init__(self) -> None:
		self.instructions: list[VirtualMachine.VMCommand] = []
	def load_program(self, program: VirtualMachine.VMProgram):
		writer = CodeWriter()
		for cls in program.classes:
			for function in cls.functions:
				for command in function.instructions:
					self.instructions.extend(
						writer.writeCommand(command)
					)

class CodeWriter:
	def __init__(self, memory_map: VirtualMachine.MemoryMap = VirtualMachine.MemoryMap()):
		self.map = memory_map
		self.current_file = None
		self.current_static_base = 16
		self.next_static_alloc = 16
	def writeCommand(self, command: VirtualMachine.VMCommand) -> list[AssemblyProgram.AssemblyInstruction]:
		if command.command_type == VirtualMachine.CommandType.C_ARITHMETIC:
			output = self.writeArithmetic(command)
		elif command.command_type in (VirtualMachine.CommandType.C_PUSH, VirtualMachine.CommandType.C_POP):
			output = self.writePushPop(command)
		elif command.command_type == VirtualMachine.CommandType.C_LABEL:
			output = self.writeLabel(command)
		elif command.command_type == VirtualMachine.CommandType.C_GOTO:
			output = self.writeGoto(command)
		elif command.command_type == VirtualMachine.CommandType.C_IFGOTO:
			output = self.writeIf(command)
		elif command.command_type == VirtualMachine.CommandType.C_FUNCTION:
			output = self.writeFunction(command)
		elif command.command_type == VirtualMachine.CommandType.C_CALL:
			output = self.writeCall(command)
		elif command.command_type == VirtualMachine.CommandType.C_RETURN:
			output = self.writeReturn(command)

		# Return the assembly code 
		return output
	
	def close(self) -> None:
		#* Closes the output file
		self.output_stream.close()
		return
	
	def writeArithmetic(self, command: VirtualMachine.VMCommand) -> str:
		#* Writes to the output file the assembly code that implements
		#* the given arithmetic command
		output: list[AssemblyProgram.AssemblyInstruction] = []
		output = ''
		if command.argument_1 in (VirtualMachine.ArithmeticType.A_NEGATE, VirtualMachine.ArithmeticType.A_NOT):
			#* Decrement the stack pointer
			output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

			if command.argument_1 == VirtualMachine.ArithmeticType.A_NEGATE:
				output += 'M = -M\n'
			elif command.argument_1 == VirtualMachine.ArithmeticType.A_NOT:
				output += 'M = !M\n'

			#* Increment the stack pointer
			output += '@SP\nM = M+1\n' # Increment the Stack Pointer
		elif command.argument_1 in (VirtualMachine.ArithmeticType.A_EQUALS, VirtualMachine.ArithmeticType.A_GREATER, VirtualMachine.ArithmeticType.A_LESS):
			#* Decrement the stack pointer
			output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

			#* Get the item on the top of the stack and store in D
			output += 'D = M\n'               # Store the stack value into the D register

			#* Decrement the stack pointer
			output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

			#* Perform the calculation
			branch_id = get_rand_str()
			if command.argument_1 == VirtualMachine.ArithmeticType.A_EQUALS:
				output += 'D = M-D\n'
				output += '@SP\nA = M\nM = -1\n' # set M to true
				output += f'@{branch_id}\n' # set jump location
				output += 'D; JEQ\n' # if is equal then skip set M to false
				output += '@SP\nA = M\nM = 0\n' # set M to false
				output += f'({branch_id})\n'
			elif command.argument_1 == VirtualMachine.ArithmeticType.A_GREATER:
				output += 'D = M-D\n'
				output += '@SP\nA = M\nM = -1\n' # set M to true
				output += f'@{branch_id}\n' # set jump location
				output += 'D; JGT\n' # if is greater then skip set M to false
				output += '@SP\nA = M\nM = 0\n' # set M to false
				output += f'({branch_id})\n'
			elif command.argument_1 == VirtualMachine.ArithmeticType.A_LESS:
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
			if command.argument_1 == VirtualMachine.ArithmeticType.A_ADD:
				output += 'D = D+M\n'
			elif command.argument_1 == VirtualMachine.ArithmeticType.A_SUBTRACT:
				output += 'D = M-D\n'
			elif command.argument_1 == VirtualMachine.ArithmeticType.A_AND:
				output += 'D = D&M\n'
			elif command.argument_1 == VirtualMachine.ArithmeticType.A_OR:
				output += 'D = D|M\n'
			
			#* Store the output on the stack
			output += '@SP\nA = M\n'
			output += 'M = D\n'

			#* Increment the stack pointer
			output += '@SP\nM = M+1\n' # Increment the Stack Pointer
		return output
	
	def writePushPop(self, command: VirtualMachine.VMCommand) -> str:
		#* Writes to the output file the assembly code that implements
		#* the given command, where the command is either C_PUSH or C_POP
		output = '\n'
		if command.command_type == VirtualMachine.CommandType.C_PUSH:
			#* D = Value to be pushed
			if command.argument_1 == VirtualMachine.MemorySegment.S_CONSTANT:
				output += f'@{str(command.argument_2)}\n' # Loads the constant value into the A register
				output += 'D = A\n'                       # Moves the constant from the A register into the D register
			elif command.argument_1 == VirtualMachine.MemorySegment.S_TEMP:
				output += f'@{str(5+int(command.argument_2))}\n'
				output += 'D = M\n'
			elif command.argument_1 == VirtualMachine.MemorySegment.S_POINTER:
				output += f'@{str(self.map.query(VirtualMachine.MemorySegment.S_POINTER, command.argument_2))}\n'
				output += 'D = M\n'
			elif command.argument_1 == VirtualMachine.MemorySegment.S_STATIC:
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

		elif command.command_type == VirtualMachine.CommandType.C_POP:
			if command.argument_1 in (VirtualMachine.MemorySegment.S_TEMP, VirtualMachine.MemorySegment.S_POINTER, VirtualMachine.MemorySegment.S_STATIC):
				#* Decrement the stack pointer
				output += '@SP\nM = M-1\nA = M\n' # Decrement the Stack Pointer

				#* Get the item on the top of the stack and store in D
				output += 'D = M\n'               # Store the stack value into the D register
				
				#* Calculate the address to store the value in
				if command.argument_1 == VirtualMachine.MemorySegment.S_TEMP:
					output += f'@{str(5+int(command.argument_2))}\n'
				elif command.argument_1 == VirtualMachine.MemorySegment.S_POINTER:
					output += f'@{str(self.map.query(VirtualMachine.MemorySegment.S_POINTER, command.argument_2))}\n'
				elif command.argument_1 == VirtualMachine.MemorySegment.S_STATIC:
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
		
	def setFileName(self, filename: str) -> None:
		#* Informs the CodeWriter that the translation of a new VM file has
		#* started (called by the main program)

		# Sort out the static variables
		self.current_file = filename
		self.current_static_base = self.next_static_alloc
		return

	def writeInit(self) -> None:
		#* Writes the assembly instructions that effect the bootstrap code
		#* that ititializes the VM. This code must be placed at the beginning
		#* of the generated *.asm file.
		output = '@256\nD = A\n@SP\nM = D\n'
		command = VirtualMachine.VMCommand()
		command.command_type = VirtualMachine.CommandType.C_CALL
		command.argument_1   = 'Sys.init'
		command.argument_2   = 0
		output += self.writeCall(command)

		self.output_stream.write(output)
		return

	def writeLabel(self, command: VirtualMachine.VMCommand) -> str:
		#* Writes assembly code that effects the label command
		output = '\n'
		output += f'({command.argument_1})'
		return output

	def writeGoto(self, command: VirtualMachine.VMCommand) -> str:
		#* Writes assembly code that effects the goto command
		output = '\n'
		output += f'@{command.argument_1}\n0; JEQ\n'
		return output

	def writeIf(self, command: VirtualMachine.VMCommand) -> str:
		#* Writes assembly code that effects the if-goto command
		output = '\n'
		output += '@SP\nM = M - 1\nA = M\nD = M\n' # Pop the item off the stack
		output += f'@{command.argument_1}\nD; JNE\n'
		return output

	def writeFunction(self, command: VirtualMachine.VMCommand) -> str:
		#* Writes assembly code that effects the function command
		output = '\n'
		function_name = command.argument_1
		n_vars = command.argument_2
		output += f'({function_name})\n' # Write the label so that other parts of
		                                 # the program can branch to it
		VirtualMachine.VMCommand_push_0 = '@SP\nA = M\nM = 0\n@SP\nM = M+1\n'
		output += (VirtualMachine.VMCommand_push_0 * n_vars) # Push n_vars 0s to the stack
		return output

	def writeCall(self, command: VirtualMachine.VMCommand) -> str:
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

	def writeReturn(self, command: VirtualMachine.VMCommand) -> str:
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
	#* parse command line arguments
	parser = argparse.ArgumentParser(
		prog="VM Translator",
		description="Converts VM programs into HACK assembly code",
	)
	parser.add_argument('filepath')
	parser.add_argument('-d', '--directory', action="store_true")
	parser.add_argument('--nobootloader', action="store_true")

	args = parser.parse_args()

	filepath: str = args.filepath
	is_directory: bool = args.directory
	add_bootloader: bool = not args.nobootloader


	#* Find all files with a .vm extension
	all_files = []
	for (root, dirs, files) in os.walk(filepath):
		all_files.extend(files)
	files = filter(
		lambda x : x[-3:] == '.vm',
		all_files
	)

	#* work out the filepath/name of the output file
	write_file = open(os.path.join(
		filepath, 
		[i for i in filepath.split('\\') if i][-1] ) + '.asm', 'w'
	)

	writer = CodeWriter(write_file)

	if add_bootloader:
		writer.writeInit()

	#* Init the VMProgram
	program = VirtualMachine.VMProgram()

	#* Loop through each file
	for file in files:
		read_file = open(os.path.join(filepath, file))

		writer.setFileName(read_file.name[:-2])

		#* Parse each file into a single VMProgram
		program.load_text(file[:-2], read_file.read())

	writer.close()
	