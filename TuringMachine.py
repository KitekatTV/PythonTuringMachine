import argparse
import os.path
from time import sleep

from TerminalPainter import DrawTerminal
from Compiler import CommandLists

stepMode = False
commandDelay = 1
pointerPosition = 10
selectedIndex = 9

mainArray = []
startIndex = 0

stateIndex = 0

backtrackedProgram = ""
stateLinesIndexes = []
linePointerPosition = -1

def ExecuteCommand(command: str) -> str:
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
				if status == "Halt":
					return "Halt"

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
				if status == "Halt":
					return "Halt"

				elif status == "OK":
					DrawTerminal(mainArray, startIndex, pointerPosition, stepMode)

				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
			linePointerPosition += 1
		else:
			linePointerPosition += command.count('.') + 2
			return "NoDelay"

	elif command[0] == 'C':
		stateIndex = int(command[1:])
		return "ChangeState"

	elif command[0] == 'H':
		linePointerPosition += 1
		return "Halt"

	return "OK"


def Begin(commands: list):
	global stepMode
	global mainArray
	global startIndex
	global stateIndex
	global backtrackedProgram
	global stateLinesIndexes
	global linePointerPosition

	DrawTerminal(mainArray, startIndex, pointerPosition, stepMode, False, backtrackedProgram, linePointerPosition)

	if not stepMode:
		sleep(1)

	status = "Begin"
	
	while status != "Halt":
		if backtrackedProgram:
			linePointerPosition = stateLinesIndexes[stateIndex]
		for command in commands[stateIndex]:
			status = ExecuteCommand(command)
			if status == "Halt":
				DrawTerminal(mainArray, startIndex, pointerPosition, False, True, backtrackedProgram, linePointerPosition)
				break

			elif status == "ChangeState":
				break

			elif status == "OK":
				DrawTerminal(mainArray, startIndex, pointerPosition, stepMode, False, backtrackedProgram, linePointerPosition)

			if status != "NoDelay" and not stepMode:
				sleep(commandDelay)


def ParseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('path', type=str, help='Path to program file')
	parser.add_argument('-s', '--step', action='store_true', help='Enables step-by-step mode')
	parser.add_argument('-d', '--delay', type=int, help='Set delay between steps in seconds. Does nothing in step-by-step mode')
	parser.add_argument('-r', '--raw', type=str, help='Pass raw string instead of file')
	parser.add_argument('-b', '--backtrack', action='store_true', help='Show decompiled program and currently executed line below')
	Args = parser.parse_args()
	return Args


def Entry():
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
