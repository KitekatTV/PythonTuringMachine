import curses

barTemplate = [r' _________________________________________________________________________________________ ',\
			   r'|    \                                                                               /    |',\
			   r'|_____\.___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___./_____|',\
			   r'|  >  ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   ||  <  |',\
			   r'|‾‾‾‾‾/˙‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾˙\‾‾‾‾‾|',\
			   r'|    /                                                                               \    |',\
			   r' ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ']
"""str: Tape template

Template of the tape that is drawn to terminal
"""

pointerTemplate = [r'\ /',\
				   r'_V_']
"""str: Pointer template

Template of the pointer that is drawn to terminal
"""

stepNumber = 0
"""int: Number of current step"""

done = False
"""bool: Indicates if backtracked is drawn

True if -b argument is used and backtracked program has been printed to terminal. False otherwise
"""


def DrawTerminal(numsToPrint: list, startIndex: int, pointerPos: int, stepMode: bool, halt = False, bt = "", point = -1):
	"""Handles everything related to drawing to the terminal

	Prints the tape and the pointer to the teminal.
	Fills tape cells with numbers and characters.
	Awaits the user input if step mode is enabled.
	Stops the program then `halt` is passed.

	Args:
		numsToPrint (list): list of all values on the tape

		startIndex (int): it is impossible to display the whole tape since it is infinite, so only 19 values from list beginning from the `startIndex` are shown

		pointerPos (int): current pointer position

		stepMode (bool): True if step-by-step is enabled, False otherwise

		halt (bool): stops the program when True, otherwise does nothing

		bt (str): string that contains backtracked program

		point (int): current line pointer position

	"""
	window = curses.initscr()
	curses.noecho()
	curses.cbreak()
	window.keypad(True)

	global done
	if bt != "" and not done:
		done = True
		lines = bt.split('\n')
		window.addstr(8, 1, '_' * 89)
		window.addstr(9 + len(lines), 1, '‾' * 89)
		for i in range(len(lines)):
			window.addstr(9 + i, 0, f"|  | {lines[i]}" + (' ' * (85 - len(lines[i])) + '|'))

	if bt != "" and point != -1:
		for i in range(len(bt.split('\n'))):
			window.addstr(9 + i, 1, '  ')
		window.addstr(9 + point, 1, '->')

	if halt:
		window.addstr(7, 0, "STATUS: Program has ended successfully. Press any key to exit...")
		window.clrtoeol()
		window.getch()
		curses.nocbreak()
		window.keypad(False)
		curses.echo()
		curses.endwin()
		return

	for i in range(len(barTemplate)):
		window.addstr(i, 0, barTemplate[i])

	if len(numsToPrint) < 20:
		for i in range(len(numsToPrint)):
			window.addch(3, 9 + (4 * i), str(numsToPrint[i]))
	else:
		for i in range(startIndex,startIndex + 19):
			window.addch(3, 9 + (4 * (i - startIndex)), str(numsToPrint[i]))

	window.addstr(1, 8 + (4 * (pointerPos - 1)), pointerTemplate[0])
	window.addstr(2, 8 + (4 * (pointerPos - 1)), pointerTemplate[1])

	window.refresh()

	if stepMode:
		global stepNumber
		if stepNumber == 0:
			s = "Entry"
		else:
			s = f"Step {stepNumber}"
		window.addstr(7, 0, f"STATUS: Step-by-step mode is active [{s}]. Press any key to move to the next step...")
		stepNumber += 1
		window.getch()
