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

clear(variables, *omit)
	Clears the variables in the dict provided for an object.
	If 'variables' is an object other than dict, and not built-in, it's __dict__
	member is used.
	
	All members of variables apart from those starting with '__' or included
	in omit are deleted.

cwd()
	Prints the current working directory.

copy(source, destination)
	Copies specified item(s) to another location.
	The target location must be a directory.

	arguments:
	source: Current location of item(s) to move. (Required)
	destination: Target location to move ietm(s)  (Required)
	
	
	synonymns: copy, cp

	
	
	synonymns: move, mv

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
	Eject the cd tray whose path is the one specified.
	
	The function currently only works on Windows.

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

ls(pth = "", indent = "")
	Prints the contents of the specified directory
	beginning with folders and then files, each sorted alphabetically.
	If wildcards are used in the base of the path (ending), the item(s) in the 
	directory matching the wildcard are printed.
	If the path is omitted, the default which is the current working directory
	is used.
	
	arguments:
	
	pth: The path to operate on. (Optional)
	indent: Indentation string to prefix a directory's contents.
	  Meant to be used by lsr.  (Optional)
	
	synonymns: ls, dir

lsr(pth = "", afterfirst = False, hint = "")
	Map the contents of a directory. If no path is provided, the current working
	directory is used.
	
	System files whose names match the tuples __system_names_start and __system_names_end
	at the beginning or end are omitted.
	Wildcards are supported and if used, only files matching the wildcards are listed
	
	The function uses ls to print the path to work on and the list the contents of that path.
	The function then iterates over any paths below this and recurses.
	
	arguments:
	 pth: The parent path to work on.  (Optional)
	 afterfirst: Reserved for this function's internal use.
	  It is used to check for whether the path has a hint on first call only.
	     (Not to use)
	 hint:If the path provided to this function has a wildcard, the wildcard is
	  extracted and separated from the path and the path set to its dir name so 
	  it is possible to recurse over the child paths of the dirname. The hint is then
	  joined to each path and passed to ls so only items matching the hint in each 
	  directory are printed. Reserved for use by this function only.
	      (Not to use.)
	
	
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
	Completely shuts down the computer then restarts it.
	
	synonymns: restartcomputer, restart

shutdown()
	Shuts down the local computer.
	
	
	synonymns:  shutdown, stopcomputer

start(f)
	Starts a specified file using the default set for that type of file
	If the name specified isn't an existing path but a program whose
	main process holds the name, that program is launched or launched in a new
	window if already running.
	
	arguments:
	
	f: Path of file or name of process to start. (Required)

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

import file_operations, console_operations, dir_operations
import types

initvars = vars()

for mod in file_operations, console_operations, dir_operations:
	for name, f in vars(mod).items():
		if type(f) == types.FunctionType and not name.startswith("__"):
			initvars[name] = f

del file_operations, types, console_operations, dir_operations, initvars

