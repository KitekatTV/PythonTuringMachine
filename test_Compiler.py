import pytest
import Exceptions
from Compiler import CheckForErrors

def test_write_noarg():
	with pytest.raises(Exceptions.MissingArgumentException):
		CheckForErrors("write;")

def test_write_incorrectarg():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForErrors("write(a)")

def test_write_openparenth():
	with pytest.raises(Exceptions.NotClosedParenthesesException):
		CheckForErrors("write(0")