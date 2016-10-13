"""
Functions that are mainly targeted at working directories.
"""

import os
import itertools

class InvalidPathError(OSError):
	"""
	Raised when the path specified cannot be resolved.
	"""

class InterimError(Exception):
	"""
	This is an interim error ad is always meant to be caught.
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
	

def __resolvehint(pth, hint):
	"""
	Working of __resolvehint:
	
	hint is checked to be a wildcard.If it is, __resolvefromdirlist is called 
	with the hintpos parameter corresponding with the location of the
	wildcard.
	The resultant generator is then returned by this function.
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
		#os.path.abspath(pth).split("\\") below will result in the first value
		#of piece being the drive therefore __resolvehint will never be called
		#with resolvedpth being an empty string as it will at the very least
		#contain the drive
		for piece in os.path.abspath(pth).split("\\"):
			if "*" in piece:
				resolved_iter = __resolvehint(resolvedpth, piece)
				try:
					resolvedpth += next(resolved_iter) +"/"
				except StopIteration: raise InterimError
				
				try:
					next(resolved_iter)#make sure generator had only one value.
					raise InterimError#path resolution yielded multiple possibilities.
				except StopIteration: pass
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
	"""
	Prints the current working directory.
	"""
	
	print os.getcwd().replace("\\", "/")


def cd(pth = ""):
	"""
	If a path to a directory is specified, it moves the cwd to that directory.
	If no path is specified, it prints the current path.
	
	
	synonymns: cd, chdir
	"""
	
	if pth == "..":
		os.chdir("..")
	elif pth != "":
		os.chdir(__resolve_cdpath(pth))
	
	cwd()

chdir = cd

def __ls(pth, directory, indent = ""):
	"""
	Print the contents of a directory.
	Names in the directory that correspond to those in either __system_names_start
	or __system_names_end are omitted.
	
	All directories are printed before files, all in alphabetical order
	
	arguments:
	
	pth: The path that is being operated on. (Required)
	directory: a list or iterator containing the contents of pth.
	 This can be obtained by calling os.listdir(pth)   (Required)
	indent: String to prefix when printing names of items in the directory.
	 This was added since this function is utilized by both ls and lsr and
	 lsr requires the contents of each path it iterates to be indented one tab 
	 from the where the path is printed so one can easily contrast a path name 
	 and its contents.
	"""
	
	directory = sorted(directory, key = lambda name: name.lower())
	if not directory:
		return
	
	def get_systemfile_indexes():
		"""
		A generator of the indexes of directory with names corresponding
		to those of system files.
		"""
		
		dir_length = len(directory)
		for i in xrange(dir_length):
			if directory[i].lower().endswith(__system_names_end) or \
					directory[i].lower().startswith(__system_names_start):
				
				yield i
	
	
	for to_rem, control in zip(get_systemfile_indexes(), itertools.count()):
		directory.pop(to_rem - control)
	
	files = []
	#Print directories while skipping files and adding their indexes to 'files'
	#for later printing
	for i in directory:
		if os.path.isdir(os.path.join(pth, i)):
			print indent + i
		else:
			files.append(i)
	
	if files:
		print indent + ("\n" + indent).join(files)
	
def ls(pth = "", indent = ""):
	"""
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
	"""
	
	if not pth:
		pth = os.getcwd()
	
	if pth.find("*") != -1:
		pth = os.path.abspath(pth)
		if os.path.exists(os.path.dirname(pth)):
			contents = __resolvehint(os.path.dirname(pth), os.path.basename(os.path.abspath(pth)))
			
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

def lsr(pth = "", afterfirst = False, hint = ""):
	"""
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
	"""
	if pth == "":
		pth = os.getcwd()
	
	ls(os.path.join(pth, hint), indent = "\t")
	
	if not afterfirst and pth.find("*") != -1:
		#check for whether the path has a hint on first call only.
		name = os.path.abspath(pth)
		pth = os.path.dirname(name)
		hint = os.path.basename(name)
		afterfirst = True #Incase after altering the loop below I or anyone else forgets
		                #to explicitly give it a True value.
	
	for f in os.listdir(pth):
		fullname = os.path.join(pth, f)
		if os.path.isdir(fullname) and not (
				os.path.basename(fullname).lower().endswith(__system_names_end) or \
				os.path.basename(fullname).lower().startswith(__system_names_start)
				):
			
			lsr(fullname, afterfirst = True, hint = hint)
	
	
dir_r = lsr

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
def pushd(pth):
	"""
	Changes the current working directory to one provided and saves
	the incumbent so it can be returned to using popd.
	
	A global variable is preferred so it can be shared by both pushd and popd.
	"""
	global __pushpopobj
	__pushpopobj = PushPopD(os.getcwd(), __resolve_cdpath(pth))
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

