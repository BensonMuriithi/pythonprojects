"""
Functions that mainly target files but occasionally also directories or even programs
"""

import os
import shutil
import subprocess
import shared_content
from dir_operations import _resolvehint
from itertools import ifilterfalse
from itertools import ifilter

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


def _getfiles(location, destination = ""):
	"""
	Evaluates validity of source and destination paths. ie. source must exist
	and destination, if given, must be a directory.
	
	If wildcards occur in location, the function generates
	filenames matching the wildcard. There can be zero files that match the wildcard.
	If the location doesn't contain wildcards, it is yielded.
	"""
	
	if destination and os.path.isfile(destination):
		raise PathIsFileError("Copy or move must be to a directory not file.")
	
	location = os.path.abspath(location)
	drname, base = os.path.dirname(location), os.path.basename(location)
	
	if "*" in base:
		for i in _resolvehint(drname, base):
			yield os.path.join(drname, i)
	else:
		if not os.path.exists(location):
			raise FileLocationError("The file {} does not exist".format(location))
		yield location


@shared_content.assert_argument_type(str)
def copy(source, destination):
	"""
	Copies specified item(s) to another location.
	The target location must be a directory.
	
	arguments:
	source: Current location of item(s) to move. (Required)
	destination: Target location to move ietm(s)  (Required)
	
	
	synonymns: copy, cp
	"""
	for f in _getfiles(source, destination):
		try:
			if os.path.isfile(f):
				shutil.copy2(f, destination)
			else:
				shutil.copytree(f, destination)
		except:
			print "Copy action unsuccessful for", f

cp = copy

@shared_content.assert_argument_type(str)
def move(source, destination):
	"""
	Moves item(s) from one location to another.
	If wildcards are used, all items matching it will be moved to the target 
	location. If an error occurs while moving any item, the item is skipped and
	operation continues to the next.
	
	arguments:
	source: Current location of item(s) to move. (Required)
	destination: Target location to move ietm(s)  (Required)
	
	
	synonymns: move, mv
	"""
	
	for f in _getfiles(source):
		try:
			shutil.move(f, destination)
		except:
			print "Move action unsuccessful for", f
	
	
mv = move

@shared_content.Windowsonly
@shared_content.assert_argument_type(str)
def delete(filename, force = ""):
	"""
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
	"""
	
	if force != "f":
		subprocess.call([shared_content.recycle, filename])
	else:
		for f in _getfiles(filename):
			try:
				if os.path.isfile(f):
					os.remove(f)
				else:
					shutil.rmtree(f)
			except:
				print "Delete action unsuccessful for", f
	
rm = remove = delete

@shared_content.assert_argument_type(str)
def rename(old, new):
	"""
	Renames a file.
	
	synonymns: rename, rni
	"""
	
	os.rename(old, new)

rni = rename

@shared_content.assert_argument_type(str)
def new_item(name):
	"""
	Create a new file with specified name.
	
	arguments:
	
	name: Name of the file to create. If the file is desired to be at a path
	 other than the cwd, the name should be the path of the file to create.
	   (Required)
	  
	
	synonymns: new_item, newitem
	"""
	with open(name, "wb"):
		return

newitem = new_item #escape simple typing mistake or name confusion

@shared_content.assert_argument_type(str)
def wipe(f = ""):
	"""
	Wipes the contents of the file or directory specified.
	Wildcards should not supported for this function.
	
	If no path is specified, the console can be cleared.
	"""
	
	if os.path.isfile(f):
		with open(f, "wb"):
			return
	elif os.path.isdir(f):
		shutil.rmtree(f)
		os.mkdir(f)
	else:
		if 'y' in raw_input("Clear console? (y / n) : ").lower():
			from console_operations import cls
			cls()

@shared_content.Windowsonly
@shared_content.assert_argument_type(str)
def find(name):
	"""
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
	"""
	x = os.path.abspath(name)
	name = os.path.basename(x)
	if name.find('*') == -1:
		name = '*' + name + '*'
	
	global hit_count
	hit_count = 0
	
	print
	def _xfinder(_dirname):
		progression_tracker = 0
		
		for hit in ifilter(None, _resolvehint(_dirname, name)):
			print os.path.join(_dirname, hit)
			progression_tracker += 1
		
		if progression_tracker:
			global hit_count
			hit_count += progression_tracker
			print
		
		try:
			for f in ifilterfalse(shared_content.is_system_file, os.listdir(_dirname)):
				d = os.path.join(_dirname, f)
				if os.path.isdir(d):
					_xfinder(d)
		except WindowsError:
			pass
	
	_xfinder(os.path.dirname(x))
	print "Your search got {count} hit{s}\n".format(count = hit_count,
					s = "" if hit_count is 1 else "s")

