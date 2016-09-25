This package contains functions that are meant to provide the capabilities
of Windows Powershell on the Python Shell.

Methods are called in the python fashion but the main script system_interface.py supports
command line arguments thus "python system_interface.py ls C:/Users" will work like
invoking ls on powershell with similar arguments (ls C:/Users)


Most methods have multiple names to handle the command name differences on powershell,
cmd and other shells. ie for instance copy() responds to the names copy and cp, ls() can
be called with dir() or ls() etc.

When new operations are discovered manageable in Python they'll be included asap.