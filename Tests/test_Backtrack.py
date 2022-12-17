import pytest

from os import listdir

import sys
sys.path.append('../PythonTuringMachine')

from Backtrack import BacktrackFull
from Backtrack import BacktrackCommand

def test_backtrack_full_empty():
	assert BacktrackFull("") == ("", [])

def test_backtrack_full_short():
	assert BacktrackFull("R.W1") == ("<Entry point>\n\n0 : State {\n    >;\n    write(1);\n}\n\n",[2])

def test_backtrack_full_long():
	assert BacktrackFull("R.I1:L.L.C1:.W0/Na:R.C2:.R/H") == ("<Entry point>\n\n0 : State {\n    >;\n    if(1) {\n        <;\n        <;\n        tostate(1);\n    };\n    write(0);\n}\n\n1 : State {\n    if(!a) {\n        >;\n        tostate(2);\n    };\n    >;\n}\n\n2 : State {\n    halt;\n}\n\n", [2, 12, 20])

def test_backtrack_command_write():
	assert BacktrackCommand("W1") == ("    write(1);\n")

def test_backtrack_command_move():
	assert BacktrackCommand("R") == ("    >;\n")

def test_backtrack_command_if():
	assert BacktrackCommand("I1:R.W1:") == ("    if(1) {\n        >;\n        write(1);\n    };\n")

def test_backtrack_command_tostate():
    assert BacktrackCommand("C2") == ("    tostate(2);\n")


def test_backtrack_command_halt():
    assert BacktrackCommand("H") == ("    halt;\n")
