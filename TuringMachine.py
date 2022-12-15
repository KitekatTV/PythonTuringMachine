import argparse
import os.path
from time import sleep

from TerminalPainter import DrawTerminal
from Compiler import CommandLists

stepMode = False
"""bool: Step-by-step mode

True if step-by-step is enabled, False otherwise
"""
commandDelay = 1
"""int: Delay between commands"""

pointerPosition = 10
"""int: Current position of the pointer"""

selectedIndex = 9
"""int: Index of the element under the pointer"""

mainArray = []
"""list: A list that stores all symbols that are currently on the tape"""

startIndex = 0
"""int: it is impossible to display the whole tape since it is infinite, so only 19 values from list beginning from the `startIndex` are shown"""

stateIndex = 0
"""int: Index of current state"""

backtrackedProgram = ""
"""str: Backtracked program

A string that contains the backtracked program
"""

stateLinesIndexes = []
"""list: A list that contains numbers that point to lines where states are defined"""

linePointerPosition = -1
"""type: Position of line pointer"""


def ExecuteCommand(command: str) -> str:
	"""Executes given command

	Args:
		command (str): a command to execute

	Returns:
		 str: result of execution

	"""
	global pointerPosition
	global selectedIndex
	global mainArray
	global startIndex
	global stateIndex
	global linePointerPosition
	global backtrackedProgram

	if type(mainArray) is str:
		mainArray = list(mainArray)

	if command[0] == 'W':
		linePointerPosition += 1
		c = str(command[1])
		if command[1] == 'B':
			c = ' '
		mainArray[selectedIndex] = c

	elif command[0] == 'R':
		linePointerPosition += 1
		selectedIndex += 1

		if pointerPosition == 19:
			startIndex += 1

		if pointerPosition < 19:
			pointerPosition += 1

		if selectedIndex == len(mainArray):
			mainArray.append(' ')

	elif command[0] == 'L':
		linePointerPosition += 1
		selectedIndex -= 1

		if pointerPosition == 1 and startIndex != 0:
			startIndex -= 1

		if pointerPosition > 1:
			pointerPosition -= 1

		if selectedIndex == -1:
			mainArray.insert(0, ' ')
			selectedIndex = 0

	elif command[0] == 'I':
		linePointerPosition += 1
		if command[1] == mainArray[selectedIndex] or (command[1] == 'B' and mainArray[selectedIndex] == ' '):
			addcommands = command[3:-1].split('.')

			for a in range(len(addcommands)):
				status = ExecuteCommand(addcommands[a])
				if status == "Halt" or status == "ChangeState":
					return status

				elif status == "OK":
					DrawTerminal(mainArray, startIndex, pointerPosition, stepMode, False, backtrackedProgram, linePointerPosition)

				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
			linePointerPosition += 1
		else:
			linePointerPosition += command.count('.') + 2
			return "NoDelay"

	elif command[0] == 'N':
		linePointerPosition += 1
		if command[1] != mainArray[selectedIndex] or (command[1] == 'B' and mainArray[selectedIndex] != ' '):
			addcommands = command[3:-1].split('.')

			for a in range(len(addcommands)):
				status = ExecuteCommand(addcommands[a])
				if status == "Halt" or status == "ChangeState":
					return status

				elif status == "OK":
					DrawTerminal(mainArray, startIndex, pointerPosition, stepMode, False, backtrackedProgram, linePointerPosition)

				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
			linePointerPosition += 1
		else:
			linePointerPosition += command.count('.') + 2
			return "NoDelay"

	elif command[0] == 'C':
		linePointerPosition += 1
		stateIndex = int(command[1:])
		return "ChangeState"

	elif command[0] == 'H':
		linePointerPosition += 1
		return "Halt"

	return "OK"


def Begin(commands: list):
	"""Main method

	Calls :meth:`TerminalPainter.DrawTerminal` and :meth:`ExecuteCommand` in order to execute given commands and draw the output to the terminal.
	Also handles delays between commands if step-by-step mode is disabled

	Args:
		commands (list): list of commands to execute

	"""
	global stepMode
	global mainArray
	global startIndex
	global stateIndex
	global backtrackedProgram
	global stateLinesIndexes
	global linePointerPosition

	if backtrackedProgram:
		linePointerPosition = 0

	DrawTerminal(mainArray, startIndex, pointerPosition, stepMode, False, backtrackedProgram, linePointerPosition)

	if not stepMode:
		sleep(1)

	status = "Begin"
	
	while status != "Halt":
		if backtrackedProgram:
			linePointerPosition = stateLinesIndexes[stateIndex]
		for command in commands[stateIndex]:
			status = ExecuteCommand(command)

			halt = status == "Halt"
			enableStep = stepMode & (status != "Halt" and status != "NoDelay")

			DrawTerminal(mainArray, startIndex, pointerPosition, enableStep, halt, backtrackedProgram, linePointerPosition)
			if status == "Halt" or status == "ChangeState":
				break

			if status != "NoDelay" and not stepMode:
				sleep(commandDelay)


def ParseArguments():
	"""Uses argparse library methods to parse command-line arguments

	Detailed description

	Returns:
		dict: A dictionary that contains all parsed arguments

	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('path', type=str, help='Path to program file')
	parser.add_argument('-s', '--step', action='store_true', help='Enables step-by-step mode')
	parser.add_argument('-d', '--delay', type=int, help='Set delay between steps in seconds. Does nothing in step-by-step mode')
	parser.add_argument('-r', '--raw', type=str, help='Pass raw string instead of file')
	parser.add_argument('-b', '--backtrack', action='store_true', help='Show decompiled program and currently executed line below')
	Args = parser.parse_args()
	return Args


def Entry():
	"""Program entry point

	Gets parsed arguments from methods :meth:`ParseArguments` and :meth:`Compiler.CommandLists` respectively and passes them to :meth:`Begin`

	Raises:
		FileNotFoundError: If file at path was not found

	"""
	global stepMode
	global commandDelay
	global mainArray
	global backtrackedProgram
	global stateLinesIndexes

	args = ParseArguments()
	path = args.path

	if args.step:
		stepMode=True

	if args.delay is not None:
		commandDelay = args.delay

	if not os.path.isfile(path):
		raise FileNotFoundError()

	inputSequence, commandLists, backtrackedProgram, stateLinesIndexes = CommandLists(path, args.raw, args.backtrack)

	if commandLists is not None:
		input("STATUS: Compilation successful. Press \"Enter\" to begin program execution\n")
		if type(inputSequence) is str:
			inputSequence = list(inputSequence)
		mainArray = [' '] * 9 + inputSequence
		Begin(commandLists)


if __name__ == "__main__":
	Entry()
