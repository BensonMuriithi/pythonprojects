"""
Functions that are mainly targeted at working directories.
"""

import os
import itertools
import shared_content

class InvalidPathError(RuntimeError):
	"""
	Raised when the path specified cannot be resolved.
	"""

class InterimError(Exception):
	"""
	This is an interim error ad is always meant to be caught.
	A custom class is created so as to not use built-in errors and catch them
	as they could actually be raised especially after later modification.
	"""


STARTHINT, CONTAINHINT, ENDHINT = 0, 1, 2
#constants specifying how name name matching of files should be assessed.

def _is_system_file(x):
	return x.lower().endswith(shared_content._system_names_end) or \
		x.lower().startswith(shared_content._system_names_start)
	
def _resolvefromdirlist(pth, hint, hintpos):
	"""
	Resolves the names in the directory pth that match with hint as per the
	hint criteria ie whether STARTHINT, ENDHINT or CONTAINHINT
	
	The function is a generator for the names in the directory that match the hint.
	"""
	
	
	#Sacrifice succintness of a single for loop for a single comparison of hintpos
	#For loops for STARTHINT and ENDHINT can also be one function
	#with an argument to accept str.startswith or str.endswith but would be
	#less comprehensible.
	
	hint = hint.lower()
	if hintpos == STARTHINT:
		for f in os.listdir(pth):
			if f.lower().startswith(hint):
				yield f
	elif hintpos == CONTAINHINT:
		for f in os.listdir(pth):
			if f.lower().find(hint) != -1:
				yield f
	elif hintpos == ENDHINT:
		for f in os.listdir(pth):
			if f.lower().endswith(hint):
				yield f
	

def _resolvehint(pth, hint):
	"""
	Working of _resolvehint:
	
	hint is checked to be a wildcard.If it is, _resolvefromdirlist is called 
	with the hintpos parameter corresponding with the location of the
	wildcard.
	The resultant generator is then returned by this function.
	"""
	
	asterisk_atstart = hint[0] == "*"
	asterisk_atend = hint[-1] == "*"
	if asterisk_atend and not asterisk_atstart:#final character
		return _resolvefromdirlist(pth, hint[:-1], STARTHINT)
	elif asterisk_atstart and not asterisk_atend:
		return _resolvefromdirlist(pth, hint[1:], ENDHINT)
	elif asterisk_atstart and asterisk_atend:
		return _resolvefromdirlist(pth, hint[1:-1], CONTAINHINT)
	else:
		raise RuntimeError("{}\nWildcard positioned within other characters. {}".format(
					hint, "Asterisk can only be positioned at start or end : non-exclusive"))


#One can disable the try and handle of WindowsError that
#ejects the cd tray for the function to be cross-platform
@shared_content.Windowsonly
def _resolve_cdpath(pth):
	"""
	Resolves a path only for purposes of changing directory.
	The provided path can contain wildcards but must be valid ie,
	the result of the resolve must be the path to a directory.
	"""
	
	resolvedpth = ""
	try:
		#os.path.abspath(pth).split("\\") below will result in the first value
		#of piece being the drive therefore _resolvehint will never be called
		#with resolvedpth being an empty string as it will at the very least
		#contain the drive
		for piece in os.path.abspath(pth).split("\\"):
			if "*" in piece:
				resolved_iter = list(_resolvehint(resolvedpth, piece))
				if len(resolved_iter) != 1:
					raise InterimError
				resolvedpth += resolved_iter[0] + "\\"
			else:
				resolvedpth += piece + "\\"
				if os.path.isdir(resolvedpth):
					continue
				
				if len(resolvedpth) <= 3 and resolvedpth.rstrip("\\") in\
												shared_content.cddrives():
					
					from console_operations import eject
					eject(resolvedpth)
					return None
				
				raise InterimError
	
	except InterimError:
		raise InvalidPathError("{} is not a valid path.".format(pth))
	
	return resolvedpth

def cwd():
	"""
	Prints the current working directory.
	"""
	
	print os.getcwd()

@shared_content.assert_argument_type(str)
def cd(pth = ""):
	"""
	If a path to a directory is specified, it moves the cwd to that directory.
	If no path is specified, it prints the current path.
	
	
	synonymns: cd, chdir
	"""
	
	if pth == "..":
		os.chdir("..")
	elif pth != "":
		resolvedpth = _resolve_cdpath(pth)
		if resolvedpth:
			os.chdir(resolvedpth)
		else: return
	
	cwd()

chdir = cd

#no need to check argument type of internal funtions.
def _ls(pth, directory, indent = ""):
	"""
	Print the contents of a directory.
	Names in the directory that correspond to those in either
	shared_content._system_names_start or shared_content._system_names_end 
	are omitted.
	
	All directories are printed before files, all in alphabetical order
	
	arguments:
	pth: The path being operated on. (Required)
	directory: a list or iterator containing the contents of pth.
	 This can be obtained by calling os.listdir(pth)   (Required)
	indent: String to prefix when printing names of items in the directory.
	 This was added since this function is utilized by both ls and lsr and
	 lsr requires the contents of each path it iterates to be indented one tab 
	 from the where the path is printed so one can easily contrast a path name 
	 and its contents.
	"""
	
	files = []
	#Print directories while skipping files and adding them to 'files'
	#for later printing
	for i in itertools.ifilterfalse(_is_system_file,\
					sorted(directory, key = lambda name: name.lower())):
		
		if os.path.isdir(os.path.join(pth, i)):
			print indent + i
		else:
			files.append(i)
	
	if files:
		print indent + ("\n" + indent).join(files)

@shared_content.assert_argument_type(str)
def ls(pth = ""):
	"""
	Prints the contents of the specified directory
	beginning with folders and then files, each sorted alphabetically.
	If wildcards are used in the base of the path (ending), the item(s) in the 
	directory matching the wildcard are printed.
	If the path is omitted, the default which is the current working directory
	is used.
	
	arguments:
	
	pth: The path to operate on. (Optional)
	
	
	synonymns: ls, dir
	"""
	
	if "*" in pth:
		_dir = os.path.dirname(os.path.abspath(pth))
		contents = _resolvehint(_dir, os.path.basename(pth))
	else:
		_dir = pth or os.getcwd()
		contents = 0
	
	if not os.path.isdir(_dir):
		raise InvalidPathError("The directory {} does not exist.".format(_dir))
	
	print "\n%s\n" % _dir
	
	_ls(_dir, contents or os.listdir(_dir), "")
	
	print

dir = ls

@shared_content.assert_argument_type(str)
def lsr(pth = ""):
	"""
	Map the contents of a directory. If no path is provided, the current working
	directory is used.
	
	Wildcards can be used.
	
	The function lists the contents of a path that match any filter if any and recurses
	over every directory under the path.
	
	arguments:
	 pth: The parent path to work on.  (Optional)
	
	
	synonymns: lsr, dir_r
	"""
	
	def _recurse_dir(_path, hint):
		if hint:
			directory = list(_resolvehint(_path, hint))
			if directory:
				print "\n%s\n" % _path
				_ls(_path, directory, "\t")
		else:
			print "\n%s\n" % _path
			_ls(_path, os.listdir(_path), "\t")
			
		for f in os.listdir(_path):
			name = os.path.join(_path, f)
			if os.path.isdir(name) and not _is_system_file(os.path.basename(name)):
				
				_recurse_dir(name, hint)
	
	if "*" in pth:
		_dir = os.path.dirname(os.path.abspath(pth))
		_hint = os.path.basename(pth)
	else:
		_dir, _hint = pth or os.getcwd(), ""
	
	if not os.path.isdir(_dir):
		raise InvalidPathError("The directory {} does not exist.".format(_dir))
	
	_recurse_dir(_dir, _hint)
	
	print

dir_r = lsr

@shared_content.assert_argument_type(str)
def mkdir(name):
	"""
	Creates a new directory of the specified path.
	"""
	os.mkdir(name)
	print "Directory {} created.".format(os.path.abspath(name))

class PushPopD(object):
	"""
	Class for creating an object that will hold the directories involved in
	the calls of pushd and popd.
	
	popd switches the current working directory between the working directory when
	pushd is called and the directory specified to pushd.
	"""
	def __init__(self, currentpath, pushpath):
		
		self.paths = itertools.cycle((currentpath, pushpath))
		next(self.paths)#position at the path to push to.
	
	def popd(self):
		os.chdir(next(self.paths))
		cwd()


__pushpopobj = None

@shared_content.assert_argument_type(str)
def pushd(pth):
	"""
	Changes the current working directory to one provided and saves
	the incumbent so it can be returned to using popd.
	
	A global variable is preferred so it can be shared by both pushd and popd.
	"""
	global __pushpopobj
	_pth = _resolve_cdpath(pth)
	if _pth:
		__pushpopobj = PushPopD(os.getcwd(), _pth)
		__pushpopobj.popd()

def popd():
	"""
	Switches the current working directory between that before pushd
	was called and the working directory after pushd was called.
	
	Nothing happens if pushd hasn't been called.
	"""
	if __pushpopobj:
		__pushpopobj.popd()
	else:
		print "Popd unavailable."

