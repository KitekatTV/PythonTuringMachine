import curses # library for console drawing

BarTemplate = [' _________________________________________________________________________________________ ',\
			   '|    \                                                                               /    |',\
			   '|_____\.___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___./_____|',\
			   '|START |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |  END |',\
			   '|‾‾‾‾‾/˙‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾˙\‾‾‾‾‾|',\
			   '|    /                                                                               \    |',\
			   ' ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ']

PointerTemplate = ['\ /',\
				   '_V_']

StepNumber = 0
	
# Handles everything related to drawing the in terminal
def Draw(numstoprint: list, pointerpos: int, stepMode: bool, halt: bool):
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
		window.addstr(i,0,BarTemplate[i])
	
	# Adds numbers to cells
	for i in range(min(18, len(numstoprint))):
		window.addch(3, 9 + (4 * i), str(numstoprint[i]))

	# Draw the pointer
	window.addstr(1, 8 + (4 * (pointerpos - 1)), PointerTemplate[0])
	window.addstr(2, 8 + (4 * (pointerpos - 1)), PointerTemplate[1])
	
	# Refresh the window
	window.refresh()

	# Step-by-step mode
	if stepMode:
		global StepNumber
		window.addstr(7, 0, f"STATUS: Step-by-step mode is active [Step {StepNumber}]. Press any key to move to the next step...")
		StepNumber += 1
		window.getch()
	

# Calls theD Draw() function
def DrawTerminal(numstoprint: list, pointerpos: int, stepMode: bool, halt=False,):
	Draw(numstoprint, pointerpos, stepMode, halt)
