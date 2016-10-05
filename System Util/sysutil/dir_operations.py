"""
Functions that are mainly targeted at working directories.
"""

import os

class InvalidPathError(OSError):
	"""
	The path specified cannot be resolved.
	"""

class InterimError(Exception):
	"""
	This is an interim error always meant to be caught.
	A custom class is created so as to not use built-in errors and catch them
	as they could actually be raised especially after later modification.
	"""

__system_names_start = ("bootmgr", "bootnxt", "system", "skypee")
__system_names_end = (".bin", ".ini", ".sys")
#some names reserved for system files.

STARTHINT, CONTAINHINT, ENDHINT = 0, 1, 2
#constants specifying how name name matching of files should be assessed.

def __resolvefromdirlist(pth, hint, hintpos):
	"""
	Resolves the names in the directory pth that match with hint as per the
	hint criteria ie whether STARTHINT, ENDHINT or CONTAINHINT
	
	The names in the directory that match the hint and its criteria are returned
	as a list : possibles
	"""
	hint = hint.lower()
	possibles = []
	
	for f in os.listdir(pth):
		if hintpos == STARTHINT and f.lower().startswith(hint):
			possibles.append(f)
		elif hintpos == CONTAINHINT and f.lower().find(hint) != -1:
			possibles.append(f)
		elif hintpos == ENDHINT and f.lower().endswith(hint):
			possibles.append(f)
	
	return possibles

def __resolvehint(pth, hint):
	"""
	Working of __resolvehint:
	
	hint is checked to contain an asterisk. If no asterisk exists in hint, then
	the hint which is the basename of pth+hint, is meant as is so the list containing
	possible matches is returned with only hint
	
	If an asterisk is located in hint, then hint is indeed a generalization eg *.py or
	prefix* or even *this_name*
	In this case ^ __resolvefromdirlist will returned all names in the directory 
	represented by pth depending on whether the hint is a suffix, prefix or contain
	generalization. The resultant list is then returned by this function.
	"""
	asterisk_atstart = hint[0] == "*"
	asterisk_atend = hint[-1] == "*"
	if asterisk_atend and not asterisk_atstart:#final character
		return __resolvefromdirlist(pth, hint[:-1], STARTHINT)
	elif asterisk_atstart and not asterisk_atend:
		return __resolvefromdirlist(pth, hint[1:], ENDHINT)
	else:#asterisk at both start and end of hint
		return __resolvefromdirlist(pth, hint[1:-1], CONTAINHINT)

def __resolve_cdpath(pth):
	"""
	Resolves a path only for purposes of changing directory.
	The provided path can contain wildcards but must be valid ie,
	the result of the resolve must be the path to a directory.
	"""
	resolvedpth = ""
	try:
		for piece in os.path.abspath(pth).split("\\"):
			if "*" in piece:
				resolved_piece = __resolvehint(resolvedpth, piece)
				
				if len(resolved_piece) == 1:
					resolvedpth += resolved_piece[0] + "/"
				else:
					raise InterimError
			else:
				resolvedpth += piece + "/"
				if not os.path.exists(resolvedpth):
					raise InterimError
		
		if not os.path.isdir(resolvedpth):
			raise InterimError
		
	except InterimError:
		raise InvalidPathError("Path {} cannot be resolved.".format(pth))
	
	return resolvedpth

def cwd():
	"""cwd / getcwd -> prints the current working directory."""
	print os.getcwd().replace("\\", "/")


def cd(pth = ""):
	"""cd / chdir (path) -> If a path to a directory is specified, it moves the 
		cwd to that directory.
	If no path is specified, it prints the current path."""
	
	if pth == "..":
		os.chdir("..")
	elif pth != "":
		os.chdir(__resolve_cdpath(pth))
	
	cwd()

chdir = cd

def __ls(pth, directory, indent = ""):
	"""
	'Backend' function to actually sort, sift and print the contents
	of a directory.
	"""
	directory = sorted(directory, key = lambda name: name.lower())
	
	systemfiles = []
	for i in xrange(len(directory)):
		if directory[i].lower().endswith(__system_names_end) or \
				directory[i].lower().startswith(__system_names_start):
			#some types of sytem files
			
			systemfiles.append(i)
	
	for to_rem, control in zip(systemfiles, xrange(len(systemfiles))):
		directory.pop(to_rem - control)
	
	files = []
	for i in directory:
		if os.path.isdir(os.path.join(pth, i)):
			print i
		else:
			files.append(i)
	
	if files:
		print indent + ("\n" + indent).join(files)
	
def ls(pth = "", indent = ""):
	"""
	ls / dir (path) -> prints the contents of the specified directory
	beginning with folders and then files, each sorted alphabetically.
	
	If the path is ommitted, the default which is the current working directory
	is used.
	"""
	if pth.find("*") != -1:
		pth = os.path.abspath(pth)
		if os.path.exists(os.path.dirname(pth)):
			contents = __resolvehint(os.path.dirname(pth), os.path.basename(os.path.abspath(pth)))
			if contents:
				print "\n" + os.path.dirname(pth).replace("\\", "/")
				__ls(os.path.dirname(pth), contents, indent)
		else:
			raise InvalidPathError("Asterisk (*) should only be in base of path for this operation.")
	else:
		if os.path.exists(pth):
			print "\n" + pth.replace("\\", "/") + "\n"
			__ls(pth, os.listdir(pth or os.getcwd()), indent)
		else:
			raise InvalidPathError("The path {} cannot be resolved".format(pth))

dir = ls

def lsr(pth = "", afterfirst = False, cuthint = ""):
	"""
	Map the contents of a directory
	
	System files whose names match the tuples __system_names_start and __system_names_end
	at the beginning or end are ommitted.
	
	Wildcards are supported and if used, only files matching the wildcards are listed
	"""
	if pth == "":
		pth = os.getcwd()
	
	ls(os.path.join(pth, cuthint), indent = "\t")
	
	if not afterfirst and pth.find("*") != -1:
		#check for whether the path has a hint on first call only.
		name = os.path.abspath(pth)
		pth = os.path.dirname(name)
		cuthint = os.path.basename(name)
	
	for f in os.listdir(pth):
		fullname = os.path.join(pth, f)
		if os.path.isdir(fullname) and not (
				os.path.basename(fullname).lower().endswith(__system_names_end) or \
				os.path.basename(fullname).lower().startswith(__system_names_start)
				):
			#print "THIS IS WHY I'M NOT LISTENING", os.path.basename(fullname)
			lsr(fullname, afterfirst = True, cuthint = cuthint)
	
	
dir_r = lsr

def mkdir(name):
	"""
	mkdir(path) -> Creates a new directory of the specified path.
	"""
	os.mkdir(name)
	print "Directory {} created.".format(os.path.abspath(name))
	
class PushPopD(object):
	"""
	class for creating object that will hold the directories involved in
	the calls of pushd and popd
	
	popd switches the current working directory between the working directory when
	pushd is called and the directory specified to pushd.
	"""
	def __init__(self, currentpath, pushpath):
		from itertools import cycle
		
		self.paths = cycle((currentpath, pushpath))
		next(self.paths)#position at the path to push to.
	
	def popd(self):
		os.chdir(next(self.paths))
		cwd()

__pushpopobj = None
def pushd(pth):
	"""
	pushd(pth) -> changes the current working directory to one provided and saves
	the incumbent so it can be returned to using popd
	"""
	global __pushpopobj
	__pushpopobj = PushPopD(os.getcwd(), __resolve_cdpath(pth))
	__pushpopobj.popd()

def popd():
	"""
	popd() -> switches the current working directory between that before pushd
	was called and the working directory after pushd was called.
	
	Nothing happens if pushd hasn't been called.
	"""
	if __pushpopobj:
		__pushpopobj.popd()
	else:
		print "Popd unavailable."

