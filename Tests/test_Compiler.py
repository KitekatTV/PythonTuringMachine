import pytest
import warnings

from os import listdir

import sys
sys.path.append('../PythonTuringMachine')

import Exceptions
from Compiler import HasParseErrors
from Compiler import HasCommandErrors
from Compiler import CommandExists
from Compiler import CompileCommand
from Compiler import StateParser
from Compiler import Compile
from Compiler import CommandLists


# HasParseErrors tests
def test_has_parse_errors_correct():
	assert HasParseErrors("iseq=0101;0:State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}") == False

def test_has_parse_errors_iseq_no_arg():
	with pytest.raises(Exceptions.MissingArgumentException):
		HasParseErrors("iseq;0:State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")

def test_has_parse_errors_iseq_wrong_arg():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		HasParseErrors("iseq=FUgyus3uaKO;0:State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")

def test_has_parse_errors_iseq_no_add_arg():
	with pytest.raises(Exceptions.NoAdditionalArgumentException):
		HasParseErrors("iseq=1010,11,;0:State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")

def test_has_parse_errors_iseq_twice():
	with pytest.raises(Exceptions.RepeatedIseqException):
		HasParseErrors("iseq=11;iseq=101;0:State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")
		
#def test_has_parse_errors_iseq_no_semicolon():
#	with pytest.raises(Exceptions.MissingSemicolonException):
#		HasParseErrors("iseq=110101,11;Mystate:State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")

def test_has_parse_errors_out_of_state():
	with pytest.raises(Exceptions.OutOfStateException):
		HasParseErrors("iseq=10;0:State{>;tostate(1);}write(1);1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")

def test_has_parse_errors_state_wo_name():
	with pytest.raises(Exceptions.MissingStateNameException):
		HasParseErrors("iseq=11;State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")

def test_has_parse_errors_state_invalid_name():
	with pytest.raises(Exceptions.InvalidStateNameException):
		HasParseErrors("iseq=11;inv}alid:na{me:State{>;tostate(1);}1:State{write(1);if(!0){tostate(endstate);};}endstate:State{halt;}")


# HasCommandErrors tests
def test_write_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		HasCommandErrors("write;")

def test_write_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		HasCommandErrors("write(%)")

def test_write_not_closed_bracket():
	with pytest.raises(Exceptions.NotClosedParenthesesException):
		HasCommandErrors("write(0")

def test_write_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		HasCommandErrors("write(0)")

def test_write_correct():
	assert HasCommandErrors("write(0);") == False

def test_move_right_no_semicilon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		HasCommandErrors(">")

def test_move_right_correct():
	assert HasCommandErrors(">;") == False

def test_move_left_no_semicilon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		HasCommandErrors("<")

def test_move_left_correct():
	assert HasCommandErrors("<;") == False

def test_if_statement_no_argument():
	with pytest.raises(Exceptions.MissingArgumentException):
		HasCommandErrors("if")

def test_if_statement_incorrect_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		HasCommandErrors("if(2)")

def test_if_statement_incorrect_negative_argument():
	with pytest.raises(Exceptions.IncorrectArgumentException):
		HasCommandErrors("if(2!)")

def test_if_statement_no_body():
	with pytest.raises(Exceptions.MissingStatementBodyException):
		HasCommandErrors("if(0)")

def test_if_statement_empty_body():
	with pytest.raises(Exceptions.EmptyStatementBodyException):
		HasCommandErrors("if(0){}")

def test_if_statement_no_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		HasCommandErrors("if(0){>;}")

def test_if_statement_correct():
	assert HasCommandErrors("if(1){>;};") == False

def test_negative_if_statement_correct():
	assert HasCommandErrors("if(!0){<;};") == False

def test_halt_missing_semicolon():
	with pytest.raises(Exceptions.MissingSemicolonException):
		HasCommandErrors("halt")

def test_halt_correct():
	assert HasCommandErrors("halt;") == False


# CommandExists tests
def test_exists_write():
	assert CommandExists("write(1);") == True

def test_exists_move_right():
	assert CommandExists(">") == True

def test_exists_move_left():
	assert CommandExists("<") == True

def test_exists_if():
	assert CommandExists("if(1){}") == True

def test_exists_halt():
	assert CommandExists("halt") == True

def test_exists_tostate():
	assert CommandExists("tostate(1)") == True

def test_exists_write_similar():
	assert CommandExists("writea(1)") == False

def test_exists_tostate_similar():
	assert CommandExists("tostatea(mystate)") == False

def test_exists_move_right_similar():
	assert CommandExists(">a") == False

def test_exists_move_left_similar():
	assert CommandExists("<a") == False

def test_exists_if_similar():
	assert CommandExists("ifa(1){}") == False

def test_exists_halt_similar():
	assert CommandExists("halta") == False

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

def test_tostate_compile():
	assert CompileCommand("tostate(1)", ['0', '1']) == "C1."

def test_tostate_with_name_compile():
    assert CompileCommand("tostate(mynextstate)", ["mystate", "mynextstate"]) == "C1."


# StateParser tests
def test_parse_short():
	assert StateParser("Tests/compile_full_short_correct.txt") == ('0', ['0'], ["write(0);>;halt;"])

def test_parse_long():
	assert StateParser("Tests/compile_full_long_correct.txt") == (['0', '0', '1', '0', '1', '0', '1', ' ', '1', '0', '0', '1', '0', '1', ' ', '1', '0', '1', '0', '1', ' ', '1', '0', '0'], ['0'], ['if(!B){write(1);>;write(0);>;};if(1){>;>;>;write(B);halt;};halt;'])

def test_parse_complex():
	assert StateParser("Tests/compile_full_multistate_correct.txt") == (['0', '0', '1', '0', '1', '0', '1', ' ', '1', '0', '0', '1', '0', '1', ' ', '1', '0', '1', '0', '1', ' ', '1', '0', '0'], ["0", "1", "mystate"], ["if(!B){write(1);>;write(0);>;};tostate(1);", ">;>;write(B);tostate(mystate);", "<;halt;"])


# Compile tests
def test_compile_full_short_correct():
	assert Compile("Tests/compile_full_short_correct.txt") == ('0', ["W0.R.H."])

def test_compile_full_long_correct():
	assert Compile("Tests/compile_full_long_correct.txt") == (['0', '0', '1', '0', '1', '0', '1', ' ', '1', '0', '0', '1', '0', '1', ' ', '1', '0', '1', '0', '1', ' ', '1', '0', '0'], ["NB:W1.R.W0.R:.I1:R.R.R.WB.H:.H."])


# CommandLists tests
def test_command_list_short_correct():
	assert CommandLists("Tests/compile_full_short_correct.txt", "", False) == ('0', [['W0', 'R', 'H']], "", [])

def test_command_list_long_correct():
    assert CommandLists("Tests/compile_full_long_correct.txt", "", False) == (['0', '0', '1', '0', '1', '0', '1', ' ', '1', '0', '0', '1', '0', '1', ' ', '1', '0', '1', '0', '1', ' ', '1', '0', '0'], [['NB:W1.R.W0.R:', 'I1:R.R.R.WB.H:', 'H']], "", [])

def test_command_list_raw():
	assert CommandLists("somefile.txt", "W0.R.H.", False) == ('0', [['W0', 'R', 'H']], "", [])

def test_command_list_raw_with_input():
	assert CommandLists("somefile.txt", "S1010/W0.R.C1./Wa.C2./H.", False) == (['1', '0', '1', '0'], [['W0', 'R', 'C1'], ['Wa', 'C2'], ['H']], "", [])

# Check example programs for compile errors
@pytest.mark.filterwarnings("ignore")
def test_example_programs():
	files = listdir("Tests/ExamplePrograms")
	try:
		for file in files:
			CommandLists(f"Tests/ExamplePrograms/{file}", "", False)
	except Exceptions.CompileException:
		pytest.fail(f"Failed to compile {file}")
