import re
import warnings
import Exceptions
import Backtrack

# Makes sure states in input sequence are defined correctly. Executed before CheckForCommandErrors()
def CheckForParseErrors(data: str) -> bool:
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
	# states
	if re.search(r"(^(?<!{)[^{]*(\b(write|halt|if|tostate)\b|[<>])|(?<=})(\b(write|halt|if|tostate)\b|[<>])[^}]*$|(?=[^{}]*(\b(write|halt|if|tostate)\b|[<>])[^{}]*(?={))[^{}:]+?:State)", data): #TODO: Fix
		raise Exceptions.OutOfStateException()
	if re.search(r"(?<!:)\bState\b", data):
		raise Exceptions.MissingStateNameException()
	if re.search(r"((?<=[;}])|^(?!iseq=)[^;]+;)[^;:}{]+?[;:}{][^}]*?:\bState\b", data):
		raise Exceptions.InvalidStateNameException(re.search(r"(?<=[;}])[^;:}{]+?[;:}{][^}]*?:\bState\b", data))
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
			if c[4] == 'B':
				k = ' '
			else:
				k = c[4]
			return f"N{k}:{output[0:-1]}:."
		else:
			output = ""
			for s in re.compile(r"((?:[^;])+)").split(c[6:-1])[1::2]:
				output += CompileCommand(s, stateNames)
			if c[3] == 'B':
				k = ' '
			else:
				k = c[3]
			return f"I{k}:{output[0:-1]}:."

	# Change state
	elif re.match(r"\btostate\b\(.+?\)", c):
		return f"C{stateNames.index(c[8:-1])}."


# Parses text to two lists: one contains states' names, the other one commands in these states
def StateParser(path: str) -> tuple:
	stateNames = []
	stateCommands = []
	iSeq = '0'
	with open(path,"r") as f:
		codeText = "".join(f.read().split())
		if CheckForParseErrors(codeText):
			CheckForWarnings(codeText)
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
					stateCommands.append(parsedCode[i])

		repeatedNames = [x for x in stateNames if stateNames.count(x) > 1]
		if len(repeatedNames) > 0:
			raise Exceptions.RepeatedStateNameException(repeatedNames[0])

	return iSeq, stateNames, stateCommands


# Compiler
def Compile(path: str) -> list:
	iSeq, stateNames, stateCommands = StateParser(path)
	commandStrings = []
	for i in range(len(stateCommands)):
		if CheckForCommandErrors(stateCommands[i]):
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
def CommandLists(path: str, raw: str, backtrack: bool) -> list:
	if not raw:
		iSeq, commandStrings = Compile(path)
		if commandStrings == "":
			raise Exceptions.EmptyFileException(path)
		elif not commandStrings:
			raise Exceptions.CompileException("Unknown error")

		backtrackedProgram = ""
		nums = []
		if backtrack:
			backtrackedProgram, nums = Backtrack.BacktrackFull('/'.join(commandStrings))

		commandLists = []
		for commands in commandStrings:
			commandLists.append(re.compile(r"((?:[^.:]|:[^:]*:)+)").split(commands)[1::2])

		return iSeq, commandLists, backtrackedProgram, nums
	else:
		iSeq = '0'
		hasIseq = raw.startswith('S')

		backtrackedProgram = ""
		nums = []

		commandLists = []
		if hasIseq:
			inputWithIseq = raw.split('/')
			iSeq = list(inputWithIseq[0][1:])
			inputStrings = inputWithIseq[1:]
		else:
			inputStrings = raw.split('/')
		for commands in inputStrings:
			commandLists.append(re.compile(r"((?:[^.:]|:[^:]*:)+)").split(commands)[1::2])
		if backtrack:
			backtrackedProgram, nums = Backtrack.BacktrackFull("/".join(inputStrings))
			
		return iSeq, commandLists, backtrackedProgram, nums
