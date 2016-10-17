This package contains functions that are meant to provide many capabilities
of various command line interfaces like CMD on the Python Shell.

Methods are called in the python fashion.

Most methods have multiple names to handle the command name differences on powershell,
cmd and other shells. ie copy()  and cp() do the same thing.

Since I mainly work with Windows and currently do not have enough experience with other
platforms, some functions require Windows but untill I include support for any unsupported
platform, anyone is more than welcome to refactor the code for more platforms.
Functions that require windows are decorated with @Windowsonly

When new operations are discovered manageable in Python they'll be included asap.

Any improvements performance or otherwise ought to be pointed out.

