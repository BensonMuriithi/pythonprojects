"""
This module contains functions that are meant to provide the capabilities
of Windows Powershell to the Python Shell.

The functions have been organised into classes to maintain order and understandability 
as well as to make maintainance and development less cumbersome and confusing.

FileLocationError is the only custom exception but apart from the exceptions
raised by shutil, all exceptions in the module are IOError objects.
"""

import os
from sys import argv
import shutil

class FileLocationError(IOError): pass

class ConsoleOperations(object):
	"""Holds methods largely affecting the console."""
	
	__python_text = "Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:24:40) [MSC v.1500 64 bit (AMD64)] on win32\n\
	Type \"help\", \"copyright\", \"credits\" or \"license\" for more information."
	
	@staticmethod
	def cls():
		"""cls -> wipes all text on the shell but input history is not affected."""
		os.system("cls")
		print DirOperations.cd()
		print "\n" + ConsoleOperations.__python_text
	
	@staticmethod
	def wipe(space, *args, **kwargs):
		"""wipe(space, *namestospare, clear_field = True) -> deletes all introduced variables, modules etc from a provided namespace.
		The namespace dictionary is the first argument. If any variables, functions etc should
		not be deleted, they should be provided after the space dict as their names as strings.
		The namespace can be provided using a call of vars, locals or globals according to
		one's needs.
		Unless clear_field is specified as False, the function assumes a call is from the shell
		therefore it goes on to clear the shell text field like cls.
		"""
		
		if not isinstance(space, dict):
			space = vars(space)
			
		to_delete = [s for s in space.keys() if not (s in args or s.startswith('__'))]
		for i in to_delete:
			del space[i]
	
		if not "clear_field" in kwargs or not kwargs["clear_field"]:
			ConsoleOperations.cls()


class DirOperations(object):
	"""Contains functions that are largely targeted at directories."""
	
	@staticmethod
	def getcwd():
		"""cwd / getcwd -> prints the current working directory."""
		return os.getcwd()
	
	cwd = getcwd
	
	@staticmethod
	def ls(pth = ""):
		"""ls / dir (path) -> lists the contents of the current working directory 
			starting with folders and then files each in alphabetical order.
			
		If a specific path of a directory is given, the contents of that directory
		are listed
		"""
		if pth == "":
			pth = DirOperations.cwd()
		directory = sorted(os.listdir(pth), key = lambda name: name.lower())
		
		length = len(directory)
		indexes = []
		for i in xrange(length):
			if directory[i].lower().endswith((".bin", ".ini", ".sys")):
				indexes.append(i)
		for i in indexes:
			directory.pop(i)
			length -= 1
		
		indexes = [i for i in xrange(length) if os.path.isdir(directory[i])]
		
		for i in indexes:
			print directory[i]
		
		for i in xrange(length):
			if i not in indexes:
				print directory[i]
		
	dir = ls
	
	@staticmethod
	def lsr(pth = ""):
		"""Map all contents in a directory"""
		if pth == "":
			pth = DirOperations.cwd()
		
		notdotdot = pth != ".."
		
		for dirname, dirdirs, dirfiles in os.walk(pth):
			print dirname if notdotdot else dirname.replace("..", 
					os.path.basename(os.path.abspath(pth)))
			if dirdirs:
				print "\n\t{}\\".format("\\\n\t".join(dirdirs))
			if dirfiles:
				print "\n\t{}".format("\n\t".join([f for f in dirfiles if not 
						f.endswith((".ini", ".bin", ".sys"))]))
		print
	
	dirr = lsr
	
	@staticmethod
	def cd(pth = ""):
		"""cd / chdir (path) -> If a path to a directory is specified, it moves the 
			cwd to that directory.
		If no path is specified, it prints the current path."""
		if os.path.isdir(pth):
			os.chdir(pth)
			DirOperations.cd()
		else:
			DirOperations.cwd()
	
	chdir = cd
	
	@staticmethod
	def mkdir(name):
		"""mkdir(path) -> Creates a new directory of the specified path."""
		os.mkdir(name)


class FileOperations(object):
	"""Functions that mainly target files but occasionally also directories or even programs"""
	
	@staticmethod
	def start(f):
		"""start(filename) -> starts a specified file using the default set for that type of file
		If the name specified isn't an existing path but a program whose
		main process holds the name, that program is launched or launched in a new
		window if already running.
		"""
		
		os.startfile(f)
	
	@staticmethod
	def stop(process):
		"""Forcefully kill a running process"""
		os.system("taskkill /f /t /im {}.exe".format(process))
	
	kill = stop_process = stop
	
	@staticmethod
	def __cp_mv(copy_or_move, *args):
		location, destination = args
		if not os.path.exists(location):
			raise FileLocationError("The file {} cannot be found".format(location))
		try:
			if copy_or_move == "mv":
				if os.path.isfile(location) and os.path.isfile(destination):
					with open(location, 'rb') as s, open(destination, 'ab') as t:
						t.write(s.read())
					os.remove(location)
				else:
					shutil.move(location, destination)
			else:
				if os.path.isfile(location) and os.path.isfile(destination):
					with open(location, 'rb') as s, open(destination, 'ab') as t:
						t.write(s.read())
				elif os.path.isfile(location):
					shutil.copy2(location, destination)
				else:
					shutil.copytree(location, destination)
		except Exception:
			raise IOError("{} unsuccessful.".format("Copy" if copy_or_move == "cp" else "Transfer"))
	
	
	@staticmethod
	def copy(source, destination):
		"""copy(source, destination) / cp -> copies a file or directory from one path to another"""
		FileOperations.__cp_mv("cp", source, destination)
	
	cp = copy
	
	@staticmethod
	def move(source, destination):
		"""move(source, destination) / mv -> moves a file or directory from one file to another. If the source
		and target are bot files and not dirs, even without having the same name,
		the contents of the source are moved to the target and the source deleted.
		"""
		
		FileOperations.__cp_mv("mv", source, destination)
	
	mv = move
	
	@staticmethod
	def rename(old, new):
		"""rename(oldname, newname) / rni-> renames a file. Technique can alo be used to
		move a file by changing its path before the name
		"""
		
		os.rename(old, new)
	
	rni = rename
	
	@staticmethod
	def delete(f):
		"""delete(filename) / rem / rm -> removes a file or directory from storage
		'del' could not be used as a synonymn to prevent clash with python's 'del' keyword
		"""
		if os.path.isfile(f):
			os.remove(f)
		elif os.path.isdir(f):
			shutil.rmtree(f)
		else:
			raise FileLocationError("File {} cannot be found.\n{}".format(f,
				"Ensure that you specified the path correctly."))
	
	rm = delete
	
	@staticmethod
	def clear(f = ""):
		"""clear(filename) -> If filename points at a file or directory, the contents of
		the target are wiped but the directory or file itself not deleted.
		If filename is not provided or doesn't exist, a question of whether to
		clear the shell text field is raised. If confirmed the text field is cleared.
		"""
		
		if os.path.isfile(f):
			with open(f, "wb") as mine:
				return
		elif os.path.isdir(f):
			os.rmdir(f)
			DirOperations.mkdir(f)
		else:
			if 'y' in raw_input("Clear console? (y / n) : ").lower():
				ConsoleOperations.cls()



__functions = dict()
for group in (ConsoleOperations, DirOperations, FileOperations):
	for n, f in vars(group).items():
		if isinstance(f, staticmethod) and n.find("__") < 0:
			#get the function from the valid staticmethod
			__functions[n] = f.__func__
	
if __name__ == "__main__":
	if len(argv) > 1:
		if argv[1] in __functions:
			__functions[argv[1]](*argv[2:])
		else:
			print "Operation not supported by sysutil."

