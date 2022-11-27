import argparse
import os.path
from time import sleep

from TerminalPainter import DrawTerminal
from Compiler import CommandList

stepMode = False
commandDelay = 1 # Delay between commands execution in run mode
pointerPos = 1 # Position of segment below poiter (1-19)
selectedIndex = 0 # Index of nums array element thats is currently under the pointer

mainArray = ['B']
startIndex = 0


# Executes given command
def Act(command: str) -> str:
	global pointerPos
	global selectedIndex
	global mainArray
	global startIndex

	if command[0] == 'W':
		mainArray[selectedIndex] = str(command[1])
	elif command[0] == 'R':
		selectedIndex += 1

		if pointerPos < 19:
			pointerPos += 1

		if pointerPos == 19:
			startIndex += 1
		
		if selectedIndex == len(mainArray) - 1:
			mainArray.append('B')	
	elif command[0] == 'L':
		if selectedIndex == 0:
			return "Halt"
		else:
			selectedIndex -= 1

			if pointerPos > 1:
				pointerPos -= 1

			if pointerPos == 1:
				startIndex -= 1
	elif command[0] == 'I':
		if command[1] == mainArray[selectedIndex]:
			addcommands = command[3:-1].split('.')
			for a in range(len(addcommands)):
				status = Act(addcommands[a])
				if status == "Halt":
					return "Halt"
				elif status == "OK":
					DrawTerminal(mainArray, startIndex, pointerPos, stepMode)
				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
		else:
			return "NoDelay"
	elif command[0] == 'N':
		if command[1] != mainArray[selectedIndex]:
			addcommands = command[3:-1].split('.')
			for a in range(len(addcommands)):
				status = Act(addcommands[a])
				if status == "Halt":
					return "Halt"
				elif status == "OK":
					DrawTerminal(mainArray, startIndex, pointerPos, stepMode)
				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
		else:
			return "NoDelay"
	elif command[0] == 'H':

		return "Halt"

	return "OK"


# Calls function to execute given commands then calls function that draws in console
def Run(commands: list):
	global stepMode
	global mainArray
	global startIndex

	if commands[0][0] == 'S':
		commands[0] = commands[0][1:].replace(',','B')
		mainArray = list(commands[0])
		commands.pop(0)

	DrawTerminal(mainArray, startIndex, pointerPos, stepMode)

	if not stepMode:
		sleep(1)

	for c in commands:
		status = Act(c)
		if status == "Halt":
			DrawTerminal(mainArray, startIndex, pointerPos, False, True)
			break
		elif status == "OK":
			DrawTerminal(mainArray, startIndex, pointerPos, stepMode)
		if status != "NoDelay" and not stepMode:
			sleep(commandDelay)
	else:
		while True:
			DrawTerminal(mainArray, startIndex, pointerPos,stepMode)


# Parses terminal arguments
def ParseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('path', type=str, help='Path to program')
	parser.add_argument('-s', '--step', action='store_true', help='Enables step-by-step mode')
	parser.add_argument('-d', '--delay', type=int, help='Sets delay between steps in seconds. Does nothing in step-by-step mode')
	Args = parser.parse_args()
	return Args


# Program entry point
def Entry():
	global stepMode
	global commandDelay

	args = ParseArguments()
	path = args.path

	if args.step:
		stepMode=True

	if args.delay is not None:
		commandDelay = args.delay

	if not os.path.isfile(path):
		print(f"ERR: No such file - {path}")
		return

	commands = CommandList(path)

	if commands is not None:
		input("STATUS: Compilation successful. Press \"Enter\" to begin program execution\n")
		Run(commands)


if __name__ == "__main__":
	Entry()
