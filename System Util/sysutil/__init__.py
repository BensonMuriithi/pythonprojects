"""
This package contains functions that are meant to provide most capabilities
of Windows Powershell on the Python Shell.

The utilities can also be utilised within programs also.
"""

import file_operations, console_operations, dir_operations
import types

initvars = vars()

for mod in file_operations, console_operations, dir_operations:
	for name, f in vars(mod).items():
		if type(f) == types.FunctionType and not name.startswith("__"):
			initvars[name] = f

del file_operations, types, console_operations, dir_operations, initvars

