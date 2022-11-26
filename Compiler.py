import re

# TODO: make this method throw custom exceptions
def ThrowCompileException(s):
	print(f"ERR: Compile error - {s}")


# Makes sure all commands are written correctly. Does not check if command exists
def CheckForErrors(data: str) -> bool:
	# write
	if re.search(r"\bwrite\b[^(]", data):
		ThrowCompileException("No argument for write")
		return False
	if re.search(r"\bwrite\b\([^01B]", data):
		ThrowCompileException("Incorrect argument (not 0,1 or B)")
		return False
	if re.search(r"\bwrite\b\(.[^)]", data):
		ThrowCompileException("Parentheses are not closed")
		return False
	if re.search(r"\bwrite\b\(.\)[^;]", data):
		ThrowCompileException("; expected")
		return False
	# move pointer
	if re.search(r"[><][^;]", data):
		ThrowCompileException("; expected")
		return False
	# if
	if re.search(r"\bif\b[^(]", data):
		ThrowCompileException("No argument for if")
		return False
	if re.search(r"\bif\b\(([^01B]{2}|[01B]!)", data):
		ThrowCompileException("Incorrect argument (not 0,1 or B)")
		return False
	if re.search(r"\bif\b\(([01B]|![01B])[^)]", data):
		ThrowCompileException("Parentheses are not closed")
		return False
	if re.search(r"\bif\b\(.{1,2}\)[^{]", data):
		ThrowCompileException("No body for if argument")
		return False
	if re.search(r"\bif\b\(.{1,2}\){}", data):
		ThrowCompileException("if argument body cannot be empty")
		return False
	if re.search(r"\bif\b\(.{1,2}\){.*?}[^;]", data):
		ThrowCompileException("; expected")
		return False
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
					ThrowCompileException(f"command \"{c}\" does not exist")
					return None
				else:
					output += CompileCommand(c)
			return output
		else:
			return None

# Parses compiled program to command list
def CommandList(path: str) -> list:
	program = Compile(path)
	if program == "":
		print("ERR: File is empty")
		return None
	elif not program:
		print("FATAL: The program has exited with fatal error - Compilation failed")
		return None
	a = re.compile(r"((?:[^.:]|:[^:]*:)+)").split(program)[1::2]
	return a