import curses # library for console drawing
import math

BarTemplate = [' _________________________________________________________________________________________ ',\
			   '|    \                                                                               /    |',\
			   '|_____\.___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___./_____|',\
			   '|START |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |  END |',\
			   '|‾‾‾‾‾/˙‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾˙\‾‾‾‾‾|',\
			   '|    /                                                                               \    |',\
			   ' ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ']

PointerTemplate = ['\ /',\
				   '_V_']

stepNumber = 0
	
# Handles everything related to drawing the in terminal
def Draw(numsToPrint: list, startIndex: int, pointerPos: int, stepMode: bool, halt: bool):
	# Starts curses
	window = curses.initscr()
	curses.noecho()
	curses.cbreak()
	window.keypad(True)

	# Exits curses
	if halt:
		window.addstr(7, 0, "STATUS: Program has ended successfully. Press any key to exit...")
		window.clrtoeol()
		window.getch()
		curses.nocbreak()
		window.keypad(False)
		curses.echo()
		return

	# Draws the bar template
	for i in range(len(BarTemplate)):
		window.addstr(i, 0, BarTemplate[i])

	# Adds numbers to cells
	if len(numsToPrint) < 20:
		for i in range(len(numsToPrint)):
			window.addch(3, 9 + (4 * i), str(numsToPrint[i]))
	else:
		for i in range(startIndex,startIndex + 19):
			window.addch(3, 9 + (4 * (i - startIndex)), str(numsToPrint[i]))

	if startIndex == 0:
		window.addstr(3, 1, "START")
	elif startIndex > 9999:
		window.addstr(3, 1, "9999+")
	else:
		window.addstr(3, 1, (str(startIndex) + '.' * (5 - int(math.log10(startIndex) + 1))))

	if startIndex + 19 >= len(numsToPrint):
		window.addstr(3, 85, " END ")
	elif len(numsToPrint) - startIndex - 19 > 9999:
		window.addstr(3, 85, "9999+")
	else:
		window.addstr(3, 85, '.' * (5 - int(math.log10(len(numsToPrint) - startIndex - 19) + 1)) + str(len(numsToPrint) - startIndex - 19))

	# Draw the pointer
	window.addstr(1, 8 + (4 * (pointerPos - 1)), PointerTemplate[0])
	window.addstr(2, 8 + (4 * (pointerPos - 1)), PointerTemplate[1])

	# Refresh the window
	window.refresh()

	# Step-by-step mode
	if stepMode:
		global stepNumber
		window.addstr(7, 0, f"STATUS: Step-by-step mode is active [Step {stepNumber}]. Press any key to move to the next step...")
		stepNumber += 1
		window.getch()
	

# Calls theD Draw() function
def DrawTerminal(numsToPrint: list, startIndex:int, pointerPos: int, stepMode: bool, halt = False,):
	Draw(numsToPrint, startIndex, pointerPos, stepMode, halt)
