import pytest

import sys
sys.path.append('../PythonTuringMachine')

import Exceptions
from Compiler import CheckForErrors
from Compiler import CompileCommand
from Compiler import Compile
from Compiler import CommandList
from Compiler import CheckIfExists

# CheckForErrors tests
def test_write_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		CheckForErrors("write;")

def test_write_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForErrors("write(a)")

def test_write_not_closed_bracket():
	with pytest.raises(Exceptions.NotClosedParenthesesException):
		CheckForErrors("write(0")

def test_write_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForErrors("write(0)")

def test_write_correct():
	assert CheckForErrors("write(0);") == True

def test_move_right_no_semicilon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForErrors(">")

def test_move_right_correct():
	assert CheckForErrors(">;") == True

def test_move_left_no_semicilon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForErrors("<")

def test_move_left_correct():
	assert CheckForErrors("<;") == True

def test_if_statement_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		CheckForErrors("if")

def test_if_statement_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForErrors("if(2)")

def test_if_statement_incorrect_negative_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForErrors("if(2!)")

def test_if_statement_no_body():
	with pytest.raises(Exceptions.MissingStatementBodyException):
		CheckForErrors("if(0)")

def test_if_statement_empty_body():
	with pytest.raises(Exceptions.EmptyStatementBodyException):
		CheckForErrors("if(0){}")

def test_if_statement_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForErrors("if(0){>;}")

def test_if_statement_correct():
	assert CheckForErrors("if(1){>;};") == True

def test_negative_if_statement_correct():
	assert CheckForErrors("if(!0){<;};") == True

def test_halt_missing_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForErrors("halt")

def test_halt_correct():
	assert CheckForErrors("halt;") == True

def test_iseq_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		CheckForErrors("iseq")

def test_iseq_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForErrors("iseq=2323A")

def test_iseq_no_additional_argument():
	with pytest.raises(Exceptions.NoAdditionalArgumentException):
		CheckForErrors("iseq=101010,")

def test_iseq_repeat():
	with pytest.raises(Exceptions.RepeatedIseqException):
		CheckForErrors("iseq=01010,010;iseq=111;")

def test_iseq_incorrect_usage():
	with pytest.raises(Exceptions.IncorrectIseqUsageException):
		CheckForErrors(">;iseq=101;")

def test_iseq_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForErrors("iseq=01010,010")

def test_iseq_correct():
	assert CheckForErrors("iseq=1010;") == True

def test_iseq_multisegment_correct():
	assert CheckForErrors("iseq=1010,10101,10;") == True


# TODO: CheckForWarning tests

# TODO: CheckIfExists tests
def test_exists_write():
	assert CheckIfExists("write(1);") == True

def test_exists_move_right():
	assert CheckIfExists(">") == True

def test_exists_move_left():
	assert CheckIfExists("<") == True

def test_exists_if():
	assert CheckIfExists("if(1){}") == True

def test_exists_halt():
	assert CheckIfExists("halt") == True

def test_exists_iseq():
	assert CheckIfExists("iseq=") == True

def test_exists_write_similar():
	assert CheckIfExists("writea(1)") == False

def test_exists_move_right_similar():
	assert CheckIfExists(">a") == False

def test_exists_move_left_similar():
	assert CheckIfExists("<a") == False

def test_exists_if_similar():
	assert CheckIfExists("ifa(1){}") == False

def test_exists_halt_similar():
	assert CheckIfExists("halta") == False

def test_exists_iseq_similar():
	assert CheckIfExists("iseqa=") == False

# CompileCommand tests
def test_write_compile_0():
	assert CompileCommand("write(0)") == "W0."

def test_write_compile_1():
	assert CompileCommand("write(1)") == "W1."

def test_write_compile_B():
	assert CompileCommand("write(B)") == "WB."

def test_move_right_compile():
	assert CompileCommand(">") == "R."

def test_move_right_compile():
	assert CompileCommand("<") == "L."

def test_halt_compile():
	assert CompileCommand("halt") == "H."

def test_if_statement_0_compile():
	assert CompileCommand("if(0){>;}") == "I0:R:."

def test_if_statement_1_compile():
	assert CompileCommand("if(1){>;}") == "I1:R:."

def test_if_statement_B_compile():
	assert CompileCommand("if(B){>;}") == "IB:R:."

def test_if_statement_not_0_compile():
	assert CompileCommand("if(!0){>;}") == "N0:R:."

def test_if_statement_not_1_compile():
	assert CompileCommand("if(!1){>;}") == "N1:R:."

def test_if_statement_not_B_compile():
	assert CompileCommand("if(!B){>;}") == "NB:R:."

def test_if_statement_long_compile():
	assert CompileCommand("if(0){>;write(0);<;write(1);}") == "I0:R.W0.L.W1:."

def test_iseq_compile():
	assert CompileCommand("iseq=1010") == "S1010."

def test_iseq_long_compile():
	assert CompileCommand("iseq=1010,1111") == "S1010,1111."


# Compile tests
def test_compile_full_short_correct():
	assert Compile("Tests/compile_full_short_correct.txt") == "W0.R.H."

def test_compile_full_incorrect():
	with pytest.raises(Exceptions.CompileException):
		Compile("Tests/compile_full_short_incorrect.txt")

def test_compile_full_long_correct():
	assert Compile("Tests/compile_full_long_correct.txt") == "S0010101,100101,10101,100.NB:W1.R.W0.R:.I1:R.R.R.WB.H:.H."


# CommandList tests
def test_command_list_short_correct():
	assert CommandList("Tests/compile_full_short_correct.txt") == ['W0', 'R', 'H']

def test_command_list_incorrect():
	with pytest.raises(Exceptions.CompileException):
		CommandList("Tests/compile_full_short_incorrect.txt")

def test_command_list_empty():
	with pytest.raises(Exceptions.CompileException):
		CommandList("Tests/compile_full_empty_file.txt")

def test_command_list_long_correct():
	assert CommandList("Tests/compile_full_long_correct.txt") == ['S0010101,100101,10101,100', 'NB:W1.R.W0.R:', 'I1:R.R.R.WB.H:', 'H']