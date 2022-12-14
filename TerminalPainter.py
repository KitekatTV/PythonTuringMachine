import curses

barTemplate = [r' _________________________________________________________________________________________ ',\
			   r'|    \                                                                               /    |',\
			   r'|_____\.___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___./_____|',\
			   r'|  >  ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   ||  <  |',\
			   r'|‾‾‾‾‾/˙‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾ ‾‾‾˙\‾‾‾‾‾|',\
			   r'|    /                                                                               \    |',\
			   r' ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ']

pointerTemplate = [r'\ /',\
				   r'_V_']

stepNumber = 0
done = False


def Draw(numsToPrint: list, startIndex: int, pointerPos: int, stepMode: bool, halt: bool, bt: str, point: int):
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


def DrawTerminal(numsToPrint: list, startIndex:int, pointerPos: int, stepMode: bool, halt = False, bt = "", point = -1):
	Draw(numsToPrint, startIndex, pointerPos, stepMode, halt, bt, point)
