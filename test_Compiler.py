import pytest
import Exceptions
from Compiler import CheckForErrors

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
