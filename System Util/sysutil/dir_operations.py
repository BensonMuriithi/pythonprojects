"""
Functions that are mainly targeted at working directories.
"""

import os

try:
	from . import shared_operations
except (SystemError, ValueError):
	import shared_operations

from time import localtime, strftime


def cwd():
	"""
	Prints the current working directory.
	"""
	
	print(os.getcwd())

def _evaluatepath(p):
	results = [s for s in shared_operations.resolve_path(p) if os.path.isdir(s)]
	if len(results) is 1:
		return results[0]
	elif not results and len(p) <= 3 and p.replace("/", "\\").rstrip("\\") \
		in shared_operations.cddrives():
		
		try:
			from .console_operations import eject
		except SystemError:
			from console_operations import eject
		
		eject(p)
		return
	
	raise OSError("\n{} does not resolve to a directory.".format(p))

@shared_operations.assert_argument_type(str)
def cd(pth = ""):
	"""
	If a path to a directory is specified, it moves the cwd to that directory.
	If no path is specified, it prints the current path.
	
	
	synonymns: cd, chdir
	"""
	
	os.chdir(pth and _evaluatepath(pth) or os.curdir)
	cwd()

chdir = cd

@shared_operations.assert_argument_type(str)
@shared_operations.catch_interrupt
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
	r = os.path.dirname(pth)
	
	if r and not os.path.isdir(r):
		raise OSError("\n%s is not a directory" % r)
	
	if "*" in os.path.basename(pth):
		directory = shared_operations.resolve_path(pth)
		pth = r
	else:
		directory = (os.path.join(pth, s) for s in os.listdir(
						pth and _evaluatepath(pth) or os.curdir))
	
	print "\nDirectory:",os.path.abspath(pth or os.curdir) + "\n"
	
	for f, st in filter(None, 
			(shared_operations.stat_accessible(s) for s in directory)):
		
		print("{mod_time}\t{dir_tag:^5}\t{size_if_file:>6}\t{name}".format(
		mod_time = strftime("%c", localtime(st.st_mtime)),
		dir_tag = os.path.isdir(f) and "DIR" or "FILE",
		size_if_file = os.path.isfile(f) and st.st_size or "",
		name = os.path.basename(f)
		))
	
	print
	
	return

dir = ls

@shared_operations.assert_argument_type(str)
@shared_operations.catch_interrupt
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
	
	if "*" in os.path.dirname(pth):
		raise OSError("\n%s is not a directory" % os.dirname(pth))
	elif "*" in os.path.basename(pth) or (pth and not os.path.isdir(pth)):
		try:
			from .file_operations import find
		except SystemError:
			from file_operations import find
		
		find(pth, 0)
		
		return
	
	for root, dirs, files in os.walk(pth or os.getcwd()):
		if dirs or files:
			print("\n%s\n" % root)
			
			for f, st in filter(None, 
				(shared_operations.stat_accessible(os.path.join(root, s)) for s in dirs + files)):
									
				print("\t{mod}\t{dtag:^5}\t{file_size:>6}\t{name}".format(
					mod = strftime("%c", localtime(st.st_mtime)),
					dtag = os.path.isdir(f) and "DIR" or "FILE",
					file_size = os.path.isfile(f) and st.st_size or "",
					name = os.path.basename(f)))
			
	print


dir_r = lsr

@shared_operations.assert_argument_type(str)
def mkdir(name):
	"""
	Creates a new directory of the specified path.
	"""
	os.makedirs(name)
	print("Directory {} created.".format(os.path.abspath(name)))

class PushPopD(object):
	"""
	Store the addresses for pushd and popd functions
	"""
	from itertools import cycle
	@classmethod
	def set_push_path(cls, pushpath):
		if pushpath.replace("/", "\\").rstrip("\\") == os.getcwd().rstrip("\\"):
			try:
				next(cls.paths)
				return
			except AttributeError:
				pass
		cls.paths = cls.cycle((os.getcwd(), pushpath))
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
		print("Popd unavailable.")

@shared_operations.assert_argument_type(str)
def pushd(pth):
	"""
	Changes the current working directory to one provided and saves
	the incumbent so it can be returned to using popd.
	
	A global variable is preferred so it can be shared by both pushd and popd.
	"""
	path = _evaluatepath(pth)
	if path:
		PushPopD.set_push_path(path)
		popd()

