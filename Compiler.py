import re
import Exceptions


# Makes sure all commands are written correctly. Does not check if command exists
def CheckForErrors(data: str) -> bool:
	# write
	if re.search(r"\bwrite\b[^(]", data):
		raise Exceptions.MissingArgumentException("write")
	if re.search(r"\bwrite\b\([^01B]", data):
		raise Exceptions.IncorrectArgumentException("write")
	if re.search(r"\bwrite\b\(.[^)]", data):
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
	return True


def CheckForWarnings(data: str):
	if ";;" in data:
		print("WARN: Compile info - unnecessary ;") # TODO: false positive?
	if not "terminate" in data:
		print("WARN: Compile info - program has no end function (terminate)")


# Check if given command exists
available_commands = ["write(",">","<","if(","terminate"]
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
	elif c == "terminate": # End program
		return "T."
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
	a = re.compile(r"((?:[^.:]|:[^:]*:)+)").split(program)[1::2]
	return a
