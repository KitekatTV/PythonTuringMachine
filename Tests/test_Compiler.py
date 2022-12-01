import pytest

import sys
sys.path.append('../PythonTuringMachine')

import Exceptions
from Compiler import CheckForCommandErrors
from Compiler import CompileCommand
from Compiler import Compile
from Compiler import CommandLists
from Compiler import CheckIfExists
from Compiler import StateParser
from Compiler import CheckForWarnings
from Compiler import CheckForParseErrors

# StateParser tests
def test_parse_short():
	assert StateParser("Tests/compile_full_short_correct.txt") == ('B', ['0'], ["write(0);>;halt;"])

def test_parse_long():
	assert StateParser("Tests/compile_full_long_correct.txt") == (['0', '0', '1', '0', '1', '0', '1', 'B', '1', '0', '0', '1', '0', '1', 'B', '1', '0', '1', '0', '1', 'B', '1', '0', '0'], ['0'], ['if(!B){write(1);>;write(0);>;};if(1){>;>;>;write(B);halt;};halt;'])

def test_parse_complex():
	assert StateParser("Tests/compile_full_multistate_correct.txt") == (['0', '0', '1', '0', '1', '0', '1', 'B', '1', '0', '0', '1', '0', '1', 'B', '1', '0', '1', '0', '1', 'B', '1', '0', '0'], ["0", "1", "mystate"], ["if(!B){write(1);>;write(0);>;};tostate(1);", ">;>;write(B);tostate(mystate);", "<;halt;"])

# CheckForParseErrors tests
def test_iseq_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		CheckForParseErrors("iseq")

def test_iseq_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForParseErrors("iseq=2323A")

def test_iseq_no_additional_argument():
	with pytest.raises(Exceptions.NoAdditionalArgumentException):
		CheckForParseErrors("iseq=101010,")

def test_iseq_repeat():
	with pytest.raises(Exceptions.RepeatedIseqException):
		CheckForParseErrors("iseq=01010,010;iseq=111;")

def test_iseq_incorrect_usage():
	with pytest.raises(Exceptions.IncorrectIseqUsageException):
		CheckForParseErrors(">;iseq=101;")

def test_iseq_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForParseErrors("iseq=01010,010")

def test_iseq_correct():
	assert CheckForParseErrors("iseq=1010;") == True

def test_iseq_multisegment_correct():
	assert CheckForParseErrors("iseq=1010,10101,10;") == True

def test_command_before_state():
	with pytest.raises(Exceptions.OutOfStateException):
		CheckForParseErrors("write(1);mystate:State{}")

def test_command_after_state():
	with pytest.raises(Exceptions.OutOfStateException):
		CheckForParseErrors("mystate:State{}write(1);")

def test_command_between_states():
	with pytest.raises(Exceptions.OutOfStateException):
		CheckForParseErrors("mystate1:State{}write(1);mystate2:State{}")

def test_missing_state_name():
	with pytest.raises(Exceptions.MissingStateNameException):
		CheckForParseErrors("mystate:State{>;}State{>;}")

def test_invalid_state_name():
	with pytest.raises(Exceptions.InvalidStateNameException):
		CheckForParseErrors("mys:t{ate:State{}")

def test_state_correct():
	assert CheckForParseErrors("mystate:State{>;}") == True


# CheckForCommandErrors tests
def test_write_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		CheckForCommandErrors("write;")

def test_write_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForCommandErrors("write(a)")

def test_write_not_closed_bracket():
	with pytest.raises(Exceptions.NotClosedParenthesesException):
		CheckForCommandErrors("write(0")

def test_write_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForCommandErrors("write(0)")

def test_write_correct():
	assert CheckForCommandErrors("write(0);") == True

def test_move_right_no_semicilon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForCommandErrors(">")

def test_move_right_correct():
	assert CheckForCommandErrors(">;") == True

def test_move_left_no_semicilon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForCommandErrors("<")

def test_move_left_correct():
	assert CheckForCommandErrors("<;") == True

def test_if_statement_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		CheckForCommandErrors("if")

def test_if_statement_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForCommandErrors("if(2)")

def test_if_statement_incorrect_negative_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		CheckForCommandErrors("if(2!)")

def test_if_statement_no_body():
	with pytest.raises(Exceptions.MissingStatementBodyException):
		CheckForCommandErrors("if(0)")

def test_if_statement_empty_body():
	with pytest.raises(Exceptions.EmptyStatementBodyException):
		CheckForCommandErrors("if(0){}")

def test_if_statement_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForCommandErrors("if(0){>;}")

def test_if_statement_correct():
	assert CheckForCommandErrors("if(1){>;};") == True

def test_negative_if_statement_correct():
	assert CheckForCommandErrors("if(!0){<;};") == True

def test_halt_missing_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		CheckForCommandErrors("halt")

def test_halt_correct():
	assert CheckForCommandErrors("halt;") == True


# CheckForWarning tests
def test_double_semicolon_warn():
	with pytest.warns(Exceptions.UnnecessarySemicolonWarning):
		CheckForWarnings("write(0);;halt;")

def test_no_halt_warn():
	with pytest.warns(Exceptions.NoExitFunctionWarning):
		CheckForWarnings(">;>;")

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
	assert CompileCommand("write(0)", []) == "W0."

def test_write_compile_1():
	assert CompileCommand("write(1)", []) == "W1."

def test_write_compile_B():
	assert CompileCommand("write(B)", []) == "WB."

def test_move_right_compile():
	assert CompileCommand(">", []) == "R."

def test_move_left_compile():
	assert CompileCommand("<", []) == "L."

def test_halt_compile():
	assert CompileCommand("halt", []) == "H."

def test_if_statement_0_compile():
	assert CompileCommand("if(0){>;}", []) == "I0:R:."

def test_if_statement_1_compile():
	assert CompileCommand("if(1){>;}", []) == "I1:R:."

def test_if_statement_B_compile():
	assert CompileCommand("if(B){>;}", []) == "IB:R:."

def test_if_statement_not_0_compile():
	assert CompileCommand("if(!0){>;}", []) == "N0:R:."

def test_if_statement_not_1_compile():
	assert CompileCommand("if(!1){>;}", []) == "N1:R:."

def test_if_statement_not_B_compile():
	assert CompileCommand("if(!B){>;}", []) == "NB:R:."

def test_if_statement_long_compile():
	assert CompileCommand("if(0){>;write(0);<;write(1);}", []) == "I0:R.W0.L.W1:."


# Compile tests
def test_compile_full_short_correct():
	assert Compile("Tests/compile_full_short_correct.txt") == ('B', ["W0.R.H."])

def test_compile_full_incorrect():
	with pytest.raises(Exceptions.CompileException):
		Compile("Tests/compile_full_short_incorrect.txt")

def test_compile_full_long_correct():
	assert Compile("Tests/compile_full_long_correct.txt") == (['0', '0', '1', '0', '1', '0', '1', 'B', '1', '0', '0', '1', '0', '1', 'B', '1', '0', '1', '0', '1', 'B', '1', '0', '0'], ["NB:W1.R.W0.R:.I1:R.R.R.WB.H:.H."])


# CommandLists tests
def test_command_list_short_correct():
	assert CommandLists("Tests/compile_full_short_correct.txt") == ('B', [['W0', 'R', 'H']])

def test_command_list_incorrect():
	with pytest.raises(Exceptions.CompileException):
		CommandLists("Tests/compile_full_short_incorrect.txt")

def test_command_list_empty():
	with pytest.raises(Exceptions.CompileException):
		CommandLists("Tests/compile_full_empty_file.txt")

def test_command_list_long_correct():
	assert CommandLists("Tests/compile_full_long_correct.txt") == (['0', '0', '1', '0', '1', '0', '1', 'B', '1', '0', '0', '1', '0', '1', 'B', '1', '0', '1', '0', '1', 'B', '1', '0', '0'], [['NB:W1.R.W0.R:', 'I1:R.R.R.WB.H:', 'H']])
