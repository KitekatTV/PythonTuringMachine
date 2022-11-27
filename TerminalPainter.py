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
def Draw(numstoprint: list, startindex: int, pointerpos: int, stepMode: bool, halt: bool):
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
	if len(numstoprint) < 20:
		for i in range(len(numstoprint)):
			window.addch(3, 9 + (4 * i), str(numstoprint[i]))		
	else:
		for i in range(startindex,startindex + 19):
			window.addch(3, 9 + (4 * (i - startindex)), str(numstoprint[i]))			

	if startindex == 0:
		window.addstr(3, 1, "START")
	elif startindex > 9999:
		window.addstr(3, 1, "9999+")
	else:
		window.addstr(3, 1, (str(startindex) + '.' * (4 - startindex // 10)))

	if startindex + 19 >= len(numstoprint):
		window.addstr(3, 85, " END ")
	else:
		window.addstr(3, 85, '.' * (4 - ((len(numstoprint) - startindex - 19) // 10)) + str(len(numstoprint) - startindex - 19))

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
def DrawTerminal(numstoprint: list, startindex:int, pointerpos: int, stepMode: bool, halt=False,):
	Draw(numstoprint, startindex, pointerpos, stepMode, halt)
