import argparse
import os.path
from time import sleep

from TerminalPainter import DrawTerminal
from Compiler import CommandLists

stepMode = False
commandDelay = 1 # Delay between commands execution in run mode
pointerPos = 10 # Position of segment below poiter (1-19)
selectedIndex = 9 # Index of nums array element thats is currently under the pointer

mainArray = []
startIndex = 0

stateIndex = 0

bt = ""
nums = []
pointat = -1

# Executes given command
def Act(command: str) -> str:
	global pointerPos
	global selectedIndex
	global mainArray
	global startIndex
	global stateIndex
	global pointat
	global bt

	if type(mainArray) is str:
		mainArray = list(mainArray)

	if command[0] == 'W':
		pointat += 1
		c = str(command[1])
		if command[1] == 'B':
			c = ' '
		mainArray[selectedIndex] = c

	elif command[0] == 'R':
		pointat += 1
		selectedIndex += 1

		if pointerPos == 19:
			startIndex += 1

		if pointerPos < 19:
			pointerPos += 1

		if selectedIndex == len(mainArray):
			mainArray.append(' ')

	elif command[0] == 'L':
		pointat += 1
		selectedIndex -= 1

		if pointerPos == 1 and startIndex != 0:
			startIndex -= 1

		if pointerPos > 1:
			pointerPos -= 1

		if selectedIndex == -1:
			mainArray.insert(0, ' ')
			selectedIndex = 0

	elif command[0] == 'I':
		pointat += 1
		if command[1] == mainArray[selectedIndex] or (command[1] == 'B' and mainArray[selectedIndex] == ' '):
			addcommands = command[3:-1].split('.')

			for a in range(len(addcommands)):
				status = Act(addcommands[a])
				if status == "Halt":
					return "Halt"

				elif status == "OK":
					DrawTerminal(mainArray, startIndex, pointerPos, stepMode, False, bt, pointat)

				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
			pointat += 1
		else:
			pointat += command.count('.') + 2
			return "NoDelay"

	elif command[0] == 'N':
		pointat += 1
		if command[1] != mainArray[selectedIndex] or (command[1] == 'B' and mainArray[selectedIndex] != ' '):
			addcommands = command[3:-1].split('.')

			for a in range(len(addcommands)):
				status = Act(addcommands[a])
				if status == "Halt":
					return "Halt"

				elif status == "OK":
					DrawTerminal(mainArray, startIndex, pointerPos, stepMode)

				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
			pointat += 1
		else:
			pointat += command.count('.') + 2
			return "NoDelay"

	elif command[0] == 'C':
		stateIndex = int(command[1:])
		return "ChangeState"

	elif command[0] == 'H':
		pointat += 1
		return "Halt"

	return "OK"


# Calls function to execute given commands then calls function that draws in console
def Run(commands: list):
	global stepMode
	global mainArray
	global startIndex
	global stateIndex
	global bt
	global nums
	global pointat

	DrawTerminal(mainArray, startIndex, pointerPos, stepMode, False, bt, pointat)

	if not stepMode:
		sleep(1)

	status = "Begin"
	
	while status != "Halt":
		if bt:
			pointat = nums[stateIndex]
		for c in commands[stateIndex]:
			status = Act(c)
			if status == "Halt":
				DrawTerminal(mainArray, startIndex, pointerPos, False, True, bt, pointat)
				break

			elif status == "ChangeState":
				break

			elif status == "OK":
				DrawTerminal(mainArray, startIndex, pointerPos, stepMode, False, bt, pointat)

			if status != "NoDelay" and not stepMode:
				sleep(commandDelay)


# Parses terminal arguments
def ParseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('path', type=str, help='Path to program')
	parser.add_argument('-s', '--step', action='store_true', help='Enables step-by-step mode')
	parser.add_argument('-d', '--delay', type=int, help='Sets delay between steps in seconds. Does nothing in step-by-step mode')
	parser.add_argument('-r', '--raw', type=str, help='Raw input')
	parser.add_argument('-b', '--backtrack', action='store_true', help='Enables backtrack')
	Args = parser.parse_args()
	return Args


# Program entry point
def Entry():
	global stepMode
	global commandDelay
	global mainArray
	global bt
	global nums

	args = ParseArguments()
	path = args.path

	if args.step:
		stepMode=True

	if args.delay is not None:
		commandDelay = args.delay

	if not os.path.isfile(path):
		print(f"ERR: No such file - {path}")
		return

	iSeq, commandLists, bt, nums = CommandLists(path, args.raw, args.backtrack)

	if commandLists is not None:
		input("STATUS: Compilation successful. Press \"Enter\" to begin program execution\n")
		if type(iSeq) is str:
			iSeq = list(iSeq)
		mainArray = [' '] * 9 + iSeq
		Run(commandLists)


if __name__ == "__main__":
	Entry()
