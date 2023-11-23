import argparse, os
import JackTokeniser, CompilationEngine

def parse_file(filepath):
	def filter_output(output):
		return '\n'.join(map(lambda x : (x if x else ''), output.split('\n')))

	with open(filepath) as file:
		contents = file.read()
	tokeniser = JackTokeniser.Tokensiser(contents)
	print(tokeniser.tokens)
	compilation_engine = CompilationEngine.CompilationEngine(tokeniser)
	ast_root = compilation_engine.compileClass()
	print(filter_output(ast_root.toXML()))
	


def save_AST(AST, filepath):
	pass

if __name__ == "__main__":
	# * Single source file usage:
	# $ python JackAnalyser.py fileName.jack
	# outputs fileName.xml file

	# * Directory usage:
	# $ python JackAnalyser.py -d /directoryname/
	# outputs a .xml file for every .jack file in the directory

	parser = argparse.ArgumentParser(
		prog="VM Translator",
		description="Converts VM programs into HACK assembly code",
	)
	parser.add_argument('filepath')
	parser.add_argument('-d', '--directory', action="store_true")

	args = parser.parse_args()

	filepath = args.filepath
	is_directory = args.directory
	
	if not is_directory:
		abstract_syntax_tree = parse_file(filepath)
		save_AST(abstract_syntax_tree, filepath[filepath.rindex('.'):]+'.xml')
	else:
		for file in [f for f in os.listdir(filepath) if os.path.isfile(f)]:
			if file[file.rindex('.'):] == '.jack':
				abstract_syntax_tree = parse_file(file)
				save_AST(abstract_syntax_tree, file[file.rindex('.'):]+'.xml')

