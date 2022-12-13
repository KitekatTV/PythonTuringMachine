import re
import warnings
import Exceptions
from Backtrack import BacktrackFull

def HasParseErrors(data: str) -> bool:
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
	if re.search(r"(?>\biseq\b=[^;]+)(?!;)", data):
		raise Exceptions.MissingSemicolonException("iseq")
	if re.search(r"(^(?<!{)[^{]*(\b(write|halt|if|tostate)\b|[<>])|(?<=})(\b(write|halt|if|tostate)\b|[<>])[^}]*$|(?=[^{}]*(\b(write|halt|if|tostate)\b|[<>])[^{}]*(?={))[^{}:]+?:State)", data):
		raise Exceptions.OutOfStateException()
	if re.search(r"(?<!:)\bState\b", data):
		raise Exceptions.MissingStateNameException()
	if re.search(r"((?<=[;}])|^(?!iseq=)[^;]+;)[^;:}{]+?[;:}{][^}]*?:\bState\b", data):
		raise Exceptions.InvalidStateNameException(re.search(r"(?<=[;}])[^;:}{]+?[;:}{][^}]*?:\bState\b", data))
	return True


def HasCommandErrors(data: str) -> bool:
	if re.search(r"\bwrite\b[^(]", data):
		raise Exceptions.MissingArgumentException("write")
	if re.search(r"\bwrite\b\([^01B]", data):
		raise Exceptions.IncorrectArgumentException("write")
	if re.search(r"\bwrite\b\(.([^)]|$)", data):
		raise Exceptions.NotClosedParenthesesException("write")
	if re.search(r"\bwrite\b\(.\)(?!;)", data):
		raise Exceptions.MissingSemicolonException("write")
	if re.search(r"[><](?!;)", data):
		raise Exceptions.MissingSemicolonException("Move pointer command (\"<\" or  \">\")")
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
	if re.search(r"\bhalt\b(?!;)", data):
		raise Exceptions.MissingSemicolonException("halt")
	return True


def CommandExists(command: str) -> bool:
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


def CheckForWarnings(data: str):
	if ";;" in data:
		warnings.warn(Exceptions.UnnecessarySemicolonWarning())
	if not "halt" in data:
		warnings.warn(Exceptions.NoExitFunctionWarning())


def CompileCommand(command: str, stateNames: list) -> str:
	if re.match(r"write\(.\)$", command):
		return f"W{command[6]}."
	if command == ">":
		return "R."
	if command == "<":
		return "L."
	if command == "halt":
		return "H."
	if command.startswith("if"):
		if command[3] == '!':
			output = ""
			for subcommand in re.compile(r"((?:[^;])+)").split(command[7:-1])[1::2]:
				output += CompileCommand(subcommand, stateNames)
			return f"N{command[4]}:{output[0:-1]}:."
		else:
			output = ""
			for subcommand in re.compile(r"((?:[^;])+)").split(command[6:-1])[1::2]:
				output += CompileCommand(subcommand, stateNames)
			return f"I{command[3]}:{output[0:-1]}:."
	if re.match(r"\btostate\b\(.+?\)", command):
		return f"C{stateNames.index(command[8:-1])}."
	return ""


def StateParser(path: str) -> tuple:
	stateNames = []
	stateCommands = []
	inputSequence = '0'
	with open(path,"r") as f:
		codeText = "".join(f.read().split())
		if not HasParseErrors(codeText):
			CheckForWarnings(codeText)
			anyInputSequence = re.search(r"\biseq\b=[01,]+;", codeText)
			if anyInputSequence:
				temp = anyInputSequence.group(0)[5:-1]
				inputSequence = list(temp.replace(',', ' '))
				codeText = codeText[len(temp) + 6:]
			parsedCode = re.compile(r"((?:[^{]|{[^{]*})+)}").split(codeText)
			
			for i in range(0,len(parsedCode) - 1):
				if(i % 2 == 0):
					stateNames.append(parsedCode[i][:-1].split(':')[0])
				else:
					stateCommands.append(parsedCode[i])

		repeatedNames = [x for x in stateNames if stateNames.count(x) > 1]
		if len(repeatedNames) > 0:
			raise Exceptions.RepeatedStateNameException(repeatedNames[0])

	return inputSequence, stateNames, stateCommands


def Compile(path: str) -> tuple:
	inputSequence, stateNames, stateCommands = StateParser(path)
	commandStrings = []
	for i in range(len(stateCommands)):
		if HasCommandErrors(stateCommands[i]):
			commands = re.compile(r"((?:[^;{]|{[^}]*})+)").split(stateCommands[i])[1::2]
			output = ""
			for c in commands:
				if not CommandExists(c):
					raise Exceptions.UnknownCommandException(c)
				else:
					output += CompileCommand(c, stateNames)
			commandStrings.append(output)

	return inputSequence, commandStrings


def CommandLists(path: str, raw: str, backtrack: bool) -> tuple:
	if not raw:
		inputSequence, commandStrings = Compile(path)
		if commandStrings == "":
			raise Exceptions.EmptyFileException(path)
		elif not commandStrings:
			raise Exceptions.CompileException("Unknown error")

		backtrackedProgram = ""
		nums = []
		if backtrack:
			backtrackedProgram, nums = BacktrackFull('/'.join(commandStrings))

		commandLists = []
		for commands in commandStrings:
			commandLists.append(re.compile(r"((?:[^.:]|:[^:]*:)+)").split(commands)[1::2])

		return inputSequence, commandLists, backtrackedProgram, nums
	else:
		inputSequence = '0'
		hasInputSequence = raw.startswith('S')

		backtrackedProgram = ""
		nums = []

		commandLists = []
		if hasInputSequence:
			inputWithIseq = raw.split('/')
			inputSequence = list(inputWithIseq[0][1:])
			inputStrings = inputWithIseq[1:]
		else:
			inputStrings = raw.split('/')
		for commands in inputStrings:
			commandLists.append(re.compile(r"((?:[^.:]|:[^:]*:)+)").split(commands)[1::2])
		if backtrack:
			backtrackedProgram, nums = BacktrackFull("/".join(inputStrings))

		return inputSequence, commandLists, backtrackedProgram, nums
