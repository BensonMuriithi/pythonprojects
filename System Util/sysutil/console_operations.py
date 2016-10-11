"""
Functions that target the shell.
"""

import tempfile
import subprocess
import os
import itertools


def cls():
	"""
	Wipes all text on the shell but input history and namespace variables
	are not affected.
	"""
	import sys
	
	os.system("cls")	
	print
	
	print "Python {version} on {sys_platform}".format(
			version = sys.version, sys_platform = sys.platform,
		)
	print "Type \"help\", \"copyright\", \"credits\" or \"license\" for more information."


def start(f):
	"""
	Starts a specified file using the default set for that type of file
	If the name specified isn't an existing path but a program whose
	main process holds the name, that program is launched or launched in a new
	window if already running.
	
	arguments:
	
	f: file or process to start. (Required)
	"""
	
	os.startfile(f)

def stop(process):
	""" 
	Forcefully kill a process and all its child processes.
	
	arguments:
	
	process: name of the process to kill. (Required)
	
	
	synonymns: stop, kill, stopprocess, taskkill
	"""
	
	outputfile = tempfile.TemporaryFile()
	
	result = subprocess.call("taskkill /f /t /im".split() + ["{}.exe".format(process)],
		stdout = outputfile, stderr = outputfile)
	
	if result != 0:
		print "Kill of {}.exe unsuccessful.".format(process)

kill = stopprocess = taskkill = stop

def tasklist(process = ""):
	"""
	Get the list of running processes. 
	To simulate omitting child processes, a process name will be printed only once.
	
	arguments:
	
	process: If provided, all processes whose name matches the one provided are printed.
		(Optional)
	
	
	synonymns:tasklist, getprocess
	"""
	
	if process:
		subprocess.call("tasklist /fi \"imagename eq {}.exe\"".format(process))
		print
		return
	
	def iterate_processes():
		"""
		Generator of lines from the call of tasklist to print.
		Skips lines whose imagename has already been printed.
		"""
		f = tempfile.TemporaryFile(bufsize = 0)
		subprocess.call("tasklist", bufsize = 0, stdout = f, stderr = f)
		
		f.seek(0)
		added_names = set()#I think the below search using the 'in' keyword
		#will be faster on a set than a list.
			
		for l in f:
			exe_location = l.find(".exe")
			
			if exe_location != -1:
				if not l[:exe_location + 1] in added_names:
					added_names.add(l[:exe_location + 1])
					yield l
			else:
				yield l
	
	print "".join(iterate_processes())

getprocess = tasklist

def cat(f):
	"""
	Print the contents of a file.
	
	arguments:
	
	f: Name of file to read.  (Required)
	
	
	synonymns: cat, stream
	"""
	if not os.path.isfile(f):
		print "Can only stream files."
		return
	
	with open(f) as xjr:
		print "".join(xjr)

stream = cat

def more(f):
	"""
	Print the contents of a file 10 lines at a time.
	
	arguments:
	
	f: The file to read.   (Required)
	"""
	if not os.path.isfile(f):
		print "Can only read contents of files."
		return
	
	step = 10
	with open(f) as xfr:
		xfr.seek(0, 2)
		file_length = xfr.tell()
		xfr.seek(0)
		for p in itertools.count(0, step):
			print "".join(itertools.islice(xfr, 0, step))
			if file_length - p > step:
				raw_input("-- More --")
			else:
				break

def shutdown():
	"""
	Shuts down the local computer.
	"""
	
	if os.name == "nt":
		subprocess.call("shutdown /s")
	else:
		print "Until this functionality is added to the package for other platforms by\
			Mr Muriithi \nkindly add it yourself if you can."

def restart_computer():
	"""
	Completely shuts down the computer then restarts it.
	
	synonymns: restart_computer, restart
	"""
	
	if os.name == "nt":
		subprocess.call("shutdown /r")
	else:
		print "Until this functionality is added to the package for other platforms by\
			Mr Muriithi \nkindly add it yourself if you can."

restart = restart_computer

