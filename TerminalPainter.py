import curses # library for console drawing
#TODELETEimport math

BarTemplate = [r' _________________________________________________________________________________________ ',\
			   r'|    \                                                                               /    |',\
			   r'|_____\.___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___./_____|',\
			   r'|  >  ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   ||  <  |',\
			   r'|‾‾‾‾‾/˙‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾˙\‾‾‾‾‾|',\
			   r'|    /                                                                               \    |',\
			   r' ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ']

PointerTemplate = [r'\ /',\
				   r'_V_']

stepNumber = 0
	
# Handles everything related to drawing the in terminal
def Draw(numsToPrint: list, startIndex: int, pointerPos: int, stepMode: bool, halt: bool, bt: str, point: int):
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

    # Draw backtracked program (if exists)
	if bt != "":
		print(bt, point)
		lines = bt.split('\n')
		for l in range(len(lines)):
			window.addstr(9 + l, 1, lines[i])

	if point != -1:
		window.addstr(9 + point, 0, '>')

	# Adds numbers to cells
	if len(numsToPrint) < 20:
		for i in range(len(numsToPrint)):
			window.addch(3, 9 + (4 * i), str(numsToPrint[i]))
	else:
		for i in range(startIndex,startIndex + 19):
			window.addch(3, 9 + (4 * (i - startIndex)), str(numsToPrint[i]))

	#TODELETEif startIndex == 0:
	#TODELETE	window.addstr(3, 1, "  >  ")
	#TODELETEelif startIndex > 9999:
	#TODELETE	window.addstr(3, 1, "9999+")
	#TODELETEelse:
	#TODELETE	window.addstr(3, 1, (str(startIndex) + '.' * (5 - int(math.log10(startIndex) + 1))))

	#TODELETEif startIndex + 19 >= len(numsToPrint):
	#TODELETE	window.addstr(3, 85, " END ")
	#TODELETEelif len(numsToPrint) - startIndex - 19 > 9999:
	#TODELETE	window.addstr(3, 85, "  <  ")
	#TODELETEelse:
	#TODELETE	window.addstr(3, 85, '.' * (5 - int(math.log10(len(numsToPrint) - startIndex - 19) + 1)) + str(len(numsToPrint) - startIndex - 19))

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
def DrawTerminal(numsToPrint: list, startIndex:int, pointerPos: int, stepMode: bool, halt = False, bt = "", point = -1):
	Draw(numsToPrint, startIndex, pointerPos, stepMode, halt, bt, point)
