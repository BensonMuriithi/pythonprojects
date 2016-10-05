"""
Functions that mainly target files but occasionally also directories or even programs
"""

import os
import shutil

class PathIsFileError(IOError):
	"""
	This exception is raised when an attempt to copy or move a target to
	a file is made. This is to prevent overwriting and interfering with existing
	files.
	"""

class FileLocationError(IOError):
	""""
	This is raised when a specified location of a file is invalid.
	"""


def __cp_mv_del(copy_or_move, location, destination):
	"""
	Backbone function to copy, move or delete files.
	
	If wildcards are used in the path for location, all files matching
	the wildcard are acted upon.
	"""
	if destination and os.path.isfile(destination):
		raise PathIsFileError("Copy or move must be to a directory not file.")
	
	location = os.path.abspath(location)
	drname, base = os.path.dirname(location), os.path.basename(location)
	
	if "*" in base:
		from dir_operations import __resolvehint
		
		files = [os.path.join(drname, i) for i in 
					__resolvehint(drname, base)]
		if len(files) == 0:
			raise FileLocationError("No files match", location)
	else:
		if not os.path.exists(location):
			raise FileLocationError("The file {} does not exist".format(location))
		files = [location]
	
	for f in files:#if error occurs on any file, continue with the rest
		try:
			if copy_or_move == "Move":
				shutil.move(f, destination)
			elif copy_or_move == "Copy":
				if os.path.isfile(f):
					shutil.copy2(f, destination)
				else:
					shutil.copytree(f, destination)
			else:#Delete
				if os.path.isfile(f):
					os.remove(f)
				else:
					shutil.rmtree(f)
		except:
			print "{} unsuccessful for {}".format(copy_or_move, f)


def copy(source, destination):
	"""
	copy(source, destination) / cp -> copies a file or files(use wildcards) 
	to another location.
	
	The target destination must be a directory.
	"""
	__cp_mv_del("Copy", source, destination)

cp = copy

def move(source, destination):
	moves a file or files(use wildcards) 
	from one location to another.
	
	__cp_mv_del("Move", source, destination)

mv = move

def rename(old, new):
	"""
	rename(oldname, newname) / rni-> renames a file.
	"""
	
	os.rename(old, new)

rni = rename

def new_item(name):
	"""
	new_item(name) -> create a new file at name.
	"""
	with open(name, "wb"):
		return

def delete(f):
	"""
	delete(filename) / rem / rm -> deletes a file or directory from its location
	
	'del' could not be used as a synonymn to prevent clash with python's 'del' keyword
	"""
	
	__cp_mv_del("Delete", f, None)
	
rm = delete

def wipe(f = ""):
	"""
	wipe(filename) -> Wipes the contents of the file or directory specified.
	wildcards are not supported for this function.
	
	If no path is specified, the console can be cleared.
	"""
	
	if os.path.isfile(f):
		with open(f, "wb") as mine:
			return
	elif os.path.isdir(f):
		shutil.rmtree(f)
		os.mkdir(f)
	else:
		if 'y' in raw_input("Clear console? (y / n) : ").lower():
			from console_operations import cls
			cls()

