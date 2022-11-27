import re
import Exceptions


# Makes sure all commands are written correctly. Does not check if command exists
def CheckForErrors(data: str) -> bool:
	# write
	if re.search(r"\bwrite\b[^(]", data):
		raise Exceptions.MissingArgumentException("write")
	if re.search(r"\bwrite\b\([^01B]", data):
		raise Exceptions.IncorrectArgumentException("write")
	if re.search(r"\bwrite\b\(.([^)]|$)", data):
		raise Exceptions.NotClosedParenthesesException("write")
	if re.search(r"\bwrite\b\(.\)[^;]", data):
		raise Exceptions.MissingSemicolonException("write")
	# move pointer
	if re.search(r"[><][^;]", data):
		raise Exceptions.MissingSemicolonException("Move pointer command (\"<\" or  \">\")")
	# if
	if re.search(r"\bif\b[^(]", data):
		raise Exceptions.MissingArgumentException("if")
	if re.search(r"\bif\b\(([^01B]{2}|[01B]!)", data):
		raise Exceptions.IncorrectArgumentException("if")
	if re.search(r"\bif\b\(([01B]|![01B])[^)]", data):
		raise Exceptions.NotClosedParenthesesException("if")
	if re.search(r"\bif\b\(.{1,2}\)[^{]", data):
		raise Exceptions.MissingStatementBodyException("if")
	if re.search(r"\bif\b\(.{1,2}\){}", data):
		raise Exceptions.EmptyStatementBodyException("if")
	if re.search(r"\bif\b\(.{1,2}\){.*?}[^;]", data):
		raise Exceptions.MissingSemicolonException("if")
	# halt
	if re.search(r"\bhalt\b[^;]", data):
		raise Exceptions.MissingSemicolonException("halt")
	# input sequence
	if re.search(r"\biseq\b[^=]", data):
		raise Exceptions.MissingArgumentException("iseq")
	if re.search(r"\biseq\b=([01B,]*[^01B,;]+?)", data):
		raise Exceptions.IncorrectArgumentException("iseq")
	if re.search(r"\biseq\b=([01B]+,)+(?![01B])", data):
		raise Exceptions.NoAdditionalArgumentException()
	if re.search(r"(\biseq\b.*){2,}", data):
		raise Exceptions.RepeatedIseqException()
	if re.search(r".+\biseq\b", data):
		raise Exceptions.IncorrectIseqUsageException()
	if re.search(r"(?>\biseq\b=[^;]+)(?!;)", data): # Requires python 3.11 (2022-05-07)
		raise Exceptions.MissingSemicolonException("iseq")
	return True


def CheckForWarnings(data: str):
	if ";;" in data:
		print("WARN: Compile info - unnecessary ;") # TODO: false positive?
	if not "halt" in data:
		print("WARN: Compile info - program has no end function (terminate)")


# Check if given command exists
available_commands = ["write(",">","<","if(","halt","iseq="]
def CheckIfExists(command: str) -> bool:
	if not any(command.startswith(a) for a in available_commands):
		return False
	return True


# "Compiles" (converts) text to commands that are easier to use later
def CompileCommand(c: str) -> str:
	if re.match("write\(.\)$", c): # write()
		return f"W{c[c.find('(') + 1:len(c) - 1]}."
	elif c == ">": # Move right
		return "R."
	elif c == "<": # Move left
		return "L."
	elif c == "halt": # End program
		return "H."
	elif c.startswith("if"): # if statement
		if c[3] == '!':
			output = ""
			for s in re.compile(r"((?:[^;])+)").split(c[7:-1])[1::2]:
				output += CompileCommand(s)
			return f"N{c[4]}:{output[0:-1]}:."
		else:
			output = ""
			for s in re.compile(r"((?:[^;])+)").split(c[6:-1])[1::2]:
				output += CompileCommand(s)
			return f"I{c[3]}:{output[0:-1]}:."
	elif c.startswith("iseq="): # input sequence
		return f"S{c[5:]}."


# Compiler
def Compile(path: str) -> str:
	with open(path,"r") as f:
		inputdata = "".join(f.read().split())
		if CheckForErrors(inputdata):
			CheckForWarnings(inputdata)
			commands = re.compile(r"((?:[^;{]|{[^}]*})+)").split(inputdata)[1::2]
			output = ""
			for c in commands:
				if not CheckIfExists(c):
					raise Exceptions.UnknownCommandException(c)
				else:
					output += CompileCommand(c)
			return output


# Parses compiled program to command list
def CommandList(path: str) -> list:
	program = Compile(path)
	if program == "":
		raise Exceptions.EmptyFileException(path)
	elif not program:
		raise Exceptions.CompileException("Unknown error")

	commands = re.compile(r"((?:[^.:]|:[^:]*:)+)").split(program)[1::2]
	return commands