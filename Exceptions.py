# Compile warnings
class CompileWarning(Warning):
	def __init__(self, message):
		self.message = f"\nWARN: Compile warning >> {message}"
		super().__init__(self.message)

class UnnecessarySemicolonWarning(CompileWarning):
	def __init__(self):
		self.message = f"Unnecessary semicolon (\";\")"
		super().__init__(self.message)

class NoExitFunctionWarning(CompileWarning):
	def __init__(self):
		self.message = f"Program does not have an exit function (\"halt;\")"
		super().__init__(self.message)


# Compile exceptions
class CompileException(Exception):
	def __init__(self, message):
		self.message = f"FATAL: Compile failed >> {message}"
		super().__init__(self.message)

class MissingArgumentException(CompileException):
	def __init__(self, command):
		self.message = f"No argument for \"{command}\""
		super().__init__(self.message)

class IncorrectArgumentException(CompileException):
	def __init__(self, command):
		self.message = f"Incorrect argument for \"{command}\""
		super().__init__(self.message)

class NotClosedParenthesesException(CompileException):
	def __init__(self, command):
		self.message = f"Parentheses not closed for \"{command}\""
		super().__init__(self.message)

class MissingSemicolonException(CompileException):
	def __init__(self, command):
		self.message = f"Semicolon (;) expected (\"{command}\")"
		super().__init__(self.message)

class MissingStatementBodyException(CompileException):
	def __init__(self, command):
		self.message = f"\"{command}\" statement must have a body"
		super().__init__(self.message)

class EmptyStatementBodyException(CompileException):
	def __init__(self, command):
		self.message = f"\"{command}\" statement body cannot be empty"
		super().__init__(self.message)

class IncorrectIseqUsageException(CompileException):
	def __init__(self):
		self.message = "\"iseq\" can only be used in the beginning of the program"
		super().__init__(self.message)

class RepeatedIseqException(CompileException):
	def __init__(self):
		self.message = "\"iseq\" can only be used once"
		super().__init__(self.message)

class NoAdditionalArgumentException(CompileException):
	def __init__(self):
		self.message = "additional argument expected after \",\" for \"iseq\""
		super().__init__(self.message)

class UnknownCommandException(CompileException):
	def __init__(self, command):
		self.message = f"Unknown command \"{command}\""
		super().__init__(self.message)

class EmptyFileException(CompileException):
	def __init__(self, path):
		self.message = f"File \"{path}\" is empty"
		super().__init__(self.message)

class OutOfStateException(CompileException):
	def __init__(self):
		self.message = f"Methods or statements cannot be used outside of states"
		super().__init__(self.message)

class MissingStateNameException(CompileException):
	def __init__(self):
		self.message = f"All states must have a name"
		super().__init__(self.message)

class InvalidStateNameException(CompileException):
	def __init__(self, name):
		self.message = f"The state name is invalid (\"{name}\")"
		super().__init__(self.message)

class RepeatedStateNameException(CompileException):
	def __init__(self, name):
		self.message = f"State with the name \"{name}\" is defined already"
		super().__init__(self.message)