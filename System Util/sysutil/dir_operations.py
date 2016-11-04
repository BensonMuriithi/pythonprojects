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
	try:
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
	except WindowsError:
		yield
	

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


def _resolve_cdpath(pth):
	"""
	Resolves a path only for purposes of changing directory.
	The provided path can contain wildcards but must be valid ie,
	the result of the resolve must be the path to a directory.
	"""
	
	separator = os.name == "nt" and "\\" or "/"
	resolvedpth = ""
	try:
		for piece in os.path.abspath(pth).split(separator):
			if "*" not in piece:
				resolvedpth += piece + separator
			else:
				resolved_iter = list(_resolvehint(resolvedpth, piece))
				if len(resolved_iter) != 1:
					raise InterimError
				resolvedpth += resolved_iter[0] + separator
			
			if os.path.isdir(resolvedpth):
				continue
			
			if len(resolvedpth) <= 3 and os.name=="nt" and \
					resolvedpth.rstrip("\\") in shared_content.cddrives():
				
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
		_dir, p = os.path.split(os.path.abspath(pth))
		if not os.path.isdir(_dir):
			raise InvalidPathError("The directory {} does not exist.".format(_dir))
		contents = _resolvehint(_dir, p)
	else:
		_dir = pth or os.getcwd()
		if not os.path.isdir(_dir):
			raise InvalidPathError("The directory {} does not exist.".format(_dir))
		contents = 0
	
	print "\n%s\n" % _dir
	
	files = []
	for i in itertools.ifilterfalse(shared_content.is_system_file,
					sorted(contents or os.listdir(_dir),
							key = lambda name: name.lower())):
		
		if os.path.isdir(os.path.join(pth, i)):
			print i
		else:
			files.append(i)
	
	if files:
		print "\n".join(files)
	
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
	
	if "*" in pth:
		_dir, hint = os.path.split(os.path.abspath(pth))
	else:
		_dir, hint = pth or os.getcwd(), ""
	
	if not os.path.isdir(_dir):
		raise InvalidPathError("{} is not an existing directory".format(_dir))
	
	if hint:
		if hint.startswith("*") and hint.endswith("*"):
			func = lambda i: hint[1:-1] in i
		elif hint.startswith("*"):
			func = lambda x: x.lower().endswith(hint[1:])
		elif hint.endswith("*"):
			func = lambda x: x.lower().startswith(hint[:-1])
		else:
			raise ValueError("Wildcard cannot be within a name. {}".format(
				"it should be at the start or end. ", hint))
	else:
		func = lambda i: True
	
	for root, dirs, files in os.walk(_dir):
		d = filter(func,\
				itertools.ifilterfalse(shared_content.is_system_file, dirs))
		f = filter(func,\
				itertools.ifilterfalse(shared_content.is_system_file, files))
		
		if f or d:
			print "\n%s\n" % root
			print "\t" + "\n\t".join(d + f)
	
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
	Store the addresses for pushd and popd functions
	"""
	@classmethod
	def set_push_path(cls, pushpath):
		if pushpath.replace("/", "\\").rstrip("\\") == os.getcwd().rstrip("\\"):
			try:
				next(cls.paths)
				return
			except AttributeError:
				pass
		cls.paths = itertools.cycle((os.getcwd(), pushpath))
		next(cls.paths)
	
	@classmethod
	def get_pop_path(cls):
		return next(cls.paths)

def popd():
	"""
	Switches the current working directory between that before pushd
	was called and the working directory after pushd was called.
	
	Nothing happens if pushd hasn't been called.
	"""
	try:
		os.chdir(PushPopD.get_pop_path())
		cwd()
	except AttributeError:
		print "Popd unavailable."

@shared_content.assert_argument_type(str)
def pushd(pth):
	"""
	Changes the current working directory to one provided and saves
	the incumbent so it can be returned to using popd.
	
	A global variable is preferred so it can be shared by both pushd and popd.
	"""
	path = _resolve_cdpath(pth)
	if path:
		PushPopD.set_push_path(path)
		popd()

