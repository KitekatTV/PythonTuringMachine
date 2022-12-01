import re
import warnings
import Exceptions

# TODO: Makes sure all commands are written correctly.
def CheckForStateErrors(data: str) -> bool:
	return True

# Makes sure all commands are written correctly. Does not check if command exists
def CheckForCommandErrors(data: str) -> bool:
	# write
	if re.search(r"\bwrite\b[^(]", data):
		raise Exceptions.MissingArgumentException("write")
	if re.search(r"\bwrite\b\([^01B]", data):
		raise Exceptions.IncorrectArgumentException("write")
	if re.search(r"\bwrite\b\(.([^)]|$)", data):
		raise Exceptions.NotClosedParenthesesException("write")
	if re.search(r"\bwrite\b\(.\)(?!;)", data):
		raise Exceptions.MissingSemicolonException("write")
	# move pointer
	if re.search(r"[><](?!;)", data):
		raise Exceptions.MissingSemicolonException("Move pointer command (\"<\" or  \">\")")
	# if
	if re.search(r"\bif\b(?!\()", data):
		raise Exceptions.MissingArgumentException("if")
	if re.search(r"\bif\b\(([^01B]{2}|[01B]!)", data):
		raise Exceptions.IncorrectArgumentException("if")
	if re.search(r"\bif\b\(([01B]|![01B])[^)]", data):
		raise Exceptions.NotClosedParenthesesException("if")
	if re.search(r"\bif\b\(.{1,2}\)(?!{)", data):
		raise Exceptions.MissingStatementBodyException("if")
	if re.search(r"\bif\b\(.{1,2}\){}", data):
		raise Exceptions.EmptyStatementBodyException("if")
	if re.search(r"\bif\b\(.{1,2}\){.*?}(?!;)", data):
		raise Exceptions.MissingSemicolonException("if")
	# halt
	if re.search(r"\bhalt\b(?!;)", data):
		raise Exceptions.MissingSemicolonException("halt")
	# input sequence
	if re.search(r"\biseq\b(?!=)", data):
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
		warnings.warn(Exceptions.UnnecessarySemicolonWarning())
	if not "halt" in data:
		warnings.warn(Exceptions.NoExitFunctionWarning())


# Check if given command exists
def CheckIfExists(command: str) -> bool:
	if re.match(r"\bwrite\b\(.\)", command):
		return True
	if re.match(r">$", command):
		return True
	if re.match(r"<$", command):
		return True
	if re.match(r"\bif\b\(.{1,2}\)", command):
		return True
	if re.match(r"\bhalt\b", command):
		return True
	if re.match(r"\biseq\b=", command):
		return True
	if re.match(r"\btostate\b\(.+?\)", command):
		return True
	return False


# Compiles text to commands that are easier to use later
def CompileCommand(c: str, stateNames: list) -> str:
	# write()
	if re.match(r"write\(.\)$", c):
		return f"W{c[c.find('(') + 1:len(c) - 1]}."

	# Move right
	elif c == ">":
		return "R."

	# Move left
	elif c == "<":
		return "L."

	# End program
	elif c == "halt":
		return "H."

	# if statement
	elif c.startswith("if"):
		if c[3] == '!':
			output = ""
			for s in re.compile(r"((?:[^;])+)").split(c[7:-1])[1::2]:
				output += CompileCommand(s, stateNames)
			return f"N{c[4]}:{output[0:-1]}:."
		else:
			output = ""
			for s in re.compile(r"((?:[^;])+)").split(c[6:-1])[1::2]:
				output += CompileCommand(s, stateNames)
			return f"I{c[3]}:{output[0:-1]}:."

	# Change state
	elif re.match(r"\btostate\b\(.+?\)", c):
		return f"C{stateNames.index(c[8:-1])}."


# Parses text to two lists: one contains states' names, the other one commands in these states
def StateParser(path: str) -> tuple:
	stateNames = []
	stateCommands = []
	iSeq = 'B'
	with open(path,"r") as f:
		codeText = "".join(f.read().split())
		if CheckForStateErrors(codeText):
			trySeq = re.search(r"\biseq\b=[01,]+;", codeText)
			if trySeq:
				seq = trySeq.group(0)[5:-1]
				iSeq = list(seq.replace(',', 'B'))
				codeText = codeText[len(seq) + 6:]
			parsedCode = re.compile(r"((?:[^{]|{[^{]*})+)}").split(codeText)
			
			for i in range(0,len(parsedCode) - 1):
				if(i % 2 == 0):
					stateNames.append(parsedCode[i][:-1].split(':')[0])
				else:
					stateCommands.append(parsedCode[i][:-1])

	return iSeq, stateNames, stateCommands


# Compiler
def Compile(path: str) -> list:
	iSeq, stateNames, stateCommands = StateParser(path)
	commandStrings = []
	for i in range(len(stateCommands)):
		if CheckForCommandErrors(stateCommands[i]):
			CheckForWarnings(stateCommands[i])
			commands = re.compile(r"((?:[^;{]|{[^}]*})+)").split(stateCommands[i])[1::2]
			output = ""
			for c in commands:
				if not CheckIfExists(c):
					raise Exceptions.UnknownCommandException(c)
				else:
					output += CompileCommand(c, stateNames)
			commandStrings.append(output)

	return iSeq, commandStrings


# Parses compiled strings program to command lists
def CommandLists(path: str) -> list:
	iSeq, commandStrings = Compile(path)
	if commandStrings == "":
		raise Exceptions.EmptyFileException(path)
	elif not commandStrings:
		raise Exceptions.CompileException("Unknown error")

	commandLists = []
	for commands in commandStrings:
		commandLists.append(re.compile(r"((?:[^.:]|:[^:]*:)+)").split(commands)[1::2])
	
	return iSeq, commandLists
