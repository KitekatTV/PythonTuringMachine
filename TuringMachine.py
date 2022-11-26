import argparse
import os.path
from time import sleep

from TerminalPainter import DrawTerminal
from Compiler import CommandList

stepMode = False
commandDelay = 1 # Delay between commands execution in run mode
pointerPos = 1 # Position of segment below poiter (1-19)
selectedIndex = 0 # Index of nums array element thats is currently under the pointer
numsArray = ['B']


# Executes given command
def Act(command: str) -> str:
	global pointerPos
	global selectedIndex
	global numsArray

	if command[0] == 'W':
		numsArray[selectedIndex] = str(command[1])
	elif command[0] == 'R':
		pointerPos += 1
		selectedIndex += 1
		if selectedIndex == len(numsArray):
			numsArray.append('B')
	elif command[0] == 'L':
		if selectedIndex == 0:
			return "Halt"
		else:
			pointerPos -= 1
			selectedIndex -= 1
	elif command[0] == 'I':
		if command[1] == numsArray[selectedIndex]:
			addcommands = command[3:-1].split('.')
			for a in range(len(addcommands)):
				if Act(addcommands[a]) == "Halt":
					return "Halt"
				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
		else:
			return "NoDelay"
	elif command[0] == 'N':
		if command[1] != numsArray[selectedIndex]:
			addcommands = command[3:-1].split('.')
			for a in range(len(addcommands)):
				if Act(addcommands[a]) == "Halt":
					return "Halt"
				if a != len(addcommands) - 1 and not stepMode:
					sleep(commandDelay)
		else:
			return "NoDelay"
	elif command[0] == 'T':
		return "Halt"

	return "OK"


# Calls function to execute given commands then calls function that draws in console
def Run(commands: list):
	global stepMode

	DrawTerminal(numsArray, pointerPos,stepMode)
	sleep(1)

	for c in commands:
		status = Act(c)
		if status == "Halt":
			DrawTerminal(numsArray, pointerPos, False, True)
			break
		elif status == "OK":
			DrawTerminal(numsArray, pointerPos, stepMode)
		if status != "NoDelay" and not stepMode:
			sleep(commandDelay)
	else:
		while True:
			DrawTerminal(numsArray, pointerPos,stepMode)


# Parses terminal arguments
def ParseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('path', type=str, help='Path to program')
	Args = parser.parse_args()
	return Args


# Program entry point
def Entry():
	global stepMode
	stepMode=True #DEBUG
	path = ParseArguments().path

	if not os.path.isfile(path):
		print(f"ERR: No such file - {path}")
		return

	commands = CommandList(path)

	if commands is not None:
		input("STATUS: Compilation successful. Press \"Enter\" to begin program execution\n")
		Run(commands)


if __name__ == "__main__":
	Entry()
