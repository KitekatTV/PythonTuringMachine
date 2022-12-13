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
done = False
	
# Handles everything related to drawing the in terminal
def Draw(numsToPrint: list, startIndex: int, pointerPos: int, stepMode: bool, halt: bool, bt: str, point: int):
	# Starts curses
	window = curses.initscr()
	curses.noecho()
	curses.cbreak()
	window.keypad(True)

	# Draw backtracked program (if exists)
	global done
	if bt != "" and not done:
		done = True
		lines = bt.split('\n')
		window.addstr(8, 1, '_' * 89)
		window.addstr(9 + len(lines), 1, '‾' * 89)
		for i in range(len(lines)):
			window.addstr(9 + i, 0, '|')
			window.addstr(9 + i, 90, '|')
		for l in range(len(lines)):
			window.addstr(9 + l, 5, lines[l])
	
	for i in range(len(bt.split('\n'))):
		window.addstr(9 + i, 0, '|  | ')

	if point != -1:
		window.addstr(9 + point, 1, '->')

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
		if stepNumber == 0:
			s = "Entry"
		else:
			s = f"Step {stepNumber}"
		window.addstr(7, 0, f"STATUS: Step-by-step mode is active [{s}]. Press any key to move to the next step...")
		stepNumber += 1
		window.getch()
	

# Calls theD Draw() function
def DrawTerminal(numsToPrint: list, startIndex:int, pointerPos: int, stepMode: bool, halt = False, bt = "", point = -1):
	Draw(numsToPrint, startIndex, pointerPos, stepMode, halt, bt, point)
