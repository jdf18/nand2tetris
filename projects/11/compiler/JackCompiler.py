import argparse, os
import JackTokeniser, CompilationEngine, SymbolTable, VMWriter

def compile_file(filepath):
    with open(filepath) as file:
        contents = file.read()
    tokeniser = JackTokeniser.Tokensiser(contents)
    compilation_engine = CompilationEngine.CompilationEngine(tokeniser.tokensList)
    vm_code = compilation_engine.compileClass()
    return vm_code

def save_VMCode(mv_code, filepath):
	print(filepath)
	with open(filepath, 'w') as file:
		file.write(mv_code)
	return

if __name__ == "__main__":
	# * Single source file usage:
	# $ python JackCompiler.py fileName.jack
	# outputs fileName.vm file

	# * Directory usage:
	# $ python JackCompiler.py -d /directoryname/
	# outputs a .vm file for every .jack file in the directory

	parser = argparse.ArgumentParser(
		prog="Jack Compiler",
		description="Converts Jack programs into VM code",
	)
	parser.add_argument('filepath')
	parser.add_argument('-d', '--directory', action="store_true")

	args = parser.parse_args()

	filepath = os.path.realpath(args.filepath) + '\\'
	is_directory = args.directory
	
	if not is_directory:
		vm_code = compile_file(filepath)
		save_VMCode(vm_code, filepath[filepath.rindex('.'):]+'.vm')
	else:
		for file in [f for f in os.listdir(filepath) if (os.path.isfile(filepath + f) and f[f.rindex('.'):] == '.jack')]:
			abstract_syntax_tree = compile_file(filepath + file)
			save_VMCode(abstract_syntax_tree, filepath + file[:file.rindex('.')]+'.vm')