"""
This package contains functions that are meant to provide most capabilities
of Windows Powershell and cmd on the Python Shell.

The utilities can also be utilised within programs also.

Functions:

cat(f)
	Print the contents of a file.
	
	arguments:
	
	f: File or name of file to read.  (Required)
	
	
	synonymns: cat, stream

cd(pth = "")
	If a path to a directory is specified, it moves the cwd to that directory.
	If no path is specified, it prints the current path.
	
	
	synonymns: cd, chdir

cls()
	Wipes all text on the shell but input history and namespace variables
	are not affected.

cwd()
	Prints the current working directory.

copy(source, destination)
	Copies specified item(s) to another location.
	The target location must be a directory.

	arguments:
	source: Current location of item(s) to move. (Required)
	destination: Target location to move ietm(s)  (Required)
	
	
	synonymns: copy, cp

delete(filename, force = "")
	Deletes a items from their location.
	
	arguments:
	
	filename: the name argument of item(s) to delete. If the filename includes
	 a wildcard, all items matching it will be deleted. 
	 Wildcards in the filename will result to all item(s) matching to be moved to
	 the recycle bin. (Required)
	force: requires the value 'f' to be true. On Windows, unless provided the value 'f'
	  the item(s) specified in filename will be moved to the recycle bin.  (Optional)
	  eg  rm("tester.pyc")  move tester.pyc to recycle bin
		  rm("tester.pyc", 'f') remove tester.pyc permanently
	  
	If an error occurs when deleting a file, the file is skipped and operation
	continues to the next.
	
	
	synonymns: rm, delete, remove

eject(drive)
	Eject the cd tray of a drive specified.
	If no drive is specified, it is checked if there is exactly one drive with
	a cd tray connected to the computer and if so that cd tray is ejected.
	
	The function currently relies on an executable and only works on Windows.

find(name)
	Searches for a name within a directory.
	Any files in a directory and all its subdirectories that match the 
	string given will be printed. Subdirectories whose basename laso matched
	the string to search for are printed.
	
	Wildcars can be used but must be in the basename only ie, terminating name
	of a path. If the name is not styled into a path or is in the cwd, the name
	acts as the basename therefore can have wildcards.
	
	arguments:
	name: Name(string) to search for in the directory.(Required)
	
	synonymns: find, search

getdrives()
	Prints the info of drives connnected to the computer.
	The function currently only works on windows and utilises the wmic command
	
	synonymns: getdrives, psdrive

ls(pth = "")
	Prints the contents of the specified directory
	beginning with folders and then files, each sorted alphabetically.
	If wildcards are used in the base of the path (ending), the item(s) in the 
	directory matching the wildcard are printed.
	If the path is omitted, the default which is the current working directory
	is used.
	
	arguments:
	
	pth: The path to operate on. (Optional)
	
	synonymns: ls, dir

lsr(pth = "")
	Map the contents of a directory. If no path is provided, the current working
	directory is used.
	
	Wildcards can be used.
	
	The function lists the contents of a path that match any filter if any and recurses
	over every directory under the path.
	
	arguments:
	 pth: The parent path to work on.  (Optional)
	
	synonymns: lsr, dir_r

mkdir(name)
	Creates a new directory of the specified path.

more(f)
	Print the contents of a file 10 lines at a time.
	
	arguments:
	
	f: File or name of file to read.   (Required)

move(source, destination)
	Moves item(s) from one location to another.
	If wildcards are used, all items matching it will be moved to the target 
	location. If an error occurs while moving any item, the item is skipped and
	operation continues to the next.
	
	arguments:
	source: Current location of item(s) to move. (Required)
	destination: Target location to move ietm(s)  (Required)
	
	synonymns: move, mv

new_item(name)
	Create a new file with specified name.
	
	arguments:
	
	name: Name of the file to create. If the file is desired to be at a path
	 other than the cwd, the name should be the path of the file to create.
	   (Required)
	
	synonymns: new_item, newitem

rename(old, new)
	Renames a file.
	
	synonymns: rename, rni

restartcomputer()
	Restarts the local computer after a given time in seconds.
	
	If a positive number is provided as an argument, a timer is
	set for the computer to restart and the user is provided with a
	countdown to abort the operation.
	If a negative number or no number is given for the wait time, the wait
	time used is 15 seconds
	
	arguments:
	 wait -> A number representing the period to restart the computer after.
			If a negative number is given, the default 15 seconds is used.
	
	synonymns: restartcomputer, restart

shutdown()
	Shuts down the local computer after a given time in seconds.
	If a positive number is provided as an argument, a timer is
	set for the computer to shutdown and the user is provided with a
	countdown to abort the operation.
	If a negative number or no number is given for the wait time, the wait
	time used is 15 seconds
	
	arguments:
	 wait -> A number representing the period to shut down the computer after.
			If a negative number is given, the default 15 seconds is used.
	
	synonymns:  shutdown, stopcomputer

stop(process)
	Forcefully kill a process and all its child processes.
	
	arguments:
	
	process: name of the process to kill. (Required)
	
	
	synonymns: stop, kill, stopprocess, taskkill

tasklist(process = "")
	Get the list of running processes. 
	To simulate omitting child processes, a process name ewill be printed only once.
	
	arguments:
	
	process: If provided, all processes whose name matches the one provided are printed.
		(Optional)
	
	
	synonymns:tasklist, getprocess

wipe(f = "")
	Wipes the contents of the file or directory specified.
	Wildcards should not supported for this function.
	
	If no path is specified, the console can be cleared.

"""

try:
	from . import console_operations, dir_operations, file_operations
except ValueError:
	import console_operations, dir_operations, file_operations

import types

_modules = file_operations, console_operations, dir_operations

vars().update({name: func for mod in _modules for name, func in vars(mod).items()\
	if type(func) == types.FunctionType and not name.startswith("_")})


