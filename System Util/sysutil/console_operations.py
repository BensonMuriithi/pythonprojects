"""
Functions that target the shell.
"""

import tempfile
import subprocess
import os
import itertools
import chardet

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


def clear(variables, *omit):
	"""
	Clears the variables in the dict provided for an object.
	If 'variables' is an object other than dict, and not built-in, it's __dict__
	member is used.
	"""
	
	if not isinstance(variables, dict):
		try:
			variables = variables.__dict__
		except AttributeError:
			raise TypeException("Object of type {} does not have members or data\
				to clear.".format(variables.__class__))
	
	for x in variables.keys():
		if not x.startswith('__') and x not in omit:
			del variables[x]
	
	if 'y' in raw_input("Clear console? (y / n) >> ").lower():
		cls()



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
	
	result = subprocess.call("taskkill /f /t /im {}.exe".format(process),
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

__posix_unavailability = "Until this functionality is added to the package for other platforms \
			by Ben \nkindly add it yourself if you can."

def shutdown():
	"""
	Shuts down the local computer.
	
	
	synonymns:  shutdown, stopcomputer
	"""
	
	if os.name == "nt":
		subprocess.call("shutdown /p")
	else:
		print __posix_unavailability


stopcomputer = shutdown

def restartcomputer():
	"""
	Completely shuts down the computer then restarts it.
	
	synonymns: restartcomputer, restart
	"""
	
	if os.name == "nt":
		subprocess.call("shutdown /r -t 00")
	else:
		print __posix_unavailability

restart = restartcomputer

def getdrives():
	"""
	Prints the info of drives connnected to the computer.
	The function currently only works on windows and utilises the wmic command
	
	
	synonymns: getdrives, psdrive
	"""
	if os.name == "nt":
		namefile = tempfile.TemporaryFile(bufsize = 0)
		volumenamefile = tempfile.TemporaryFile(bufsize = 0)
		freespacefile = tempfile.TemporaryFile(bufsize = 0)
		
		#Store the result of each detail for later formatting.
		subprocess.call("wmic logicaldisk get name", stdout = namefile)
		subprocess.call("wmic logicaldisk get volumename", stdout = volumenamefile)
		subprocess.call("wmic logicaldisk get freespace", stdout = freespacefile)
		
		result_files = (namefile, volumenamefile, freespacefile)#no performance hit
		for f in result_files:
			f.seek(0)
		
		def format_cmdoutput(s):#Output of wmic is encoded in utf-16_le
			encoding = chardet.detect(s)#pypi package to detect encoding
			return s.decode(encoding["encoding"], 'ignore')[1:].rstrip()
		
		format_template = "\t{0}\t\t\t   {1}\t\t  {2}"
		#result of trial and error for best fit .join() isn't flexible enough
		
		print format_template.format(*(format_cmdoutput(f.readline()) for f in result_files))
		
		print "  {0}\t\t{1}\t\t{2}".format(*itertools.repeat("-"*15, len(result_files)))
		
		for i in itertools.izip(namefile, volumenamefile, freespacefile):
			name, vol_name, space = (x.replace("\x00", "").rstrip() for x in i)
			
			print format_template.format(name or "Unknown",#Some drives are detected
				#but aren't registered so requests for their name are blank
				
				vol_name or "Unavailable",#A drive eg dvd-rom are registered but 
				#are inactive thus no volume name
				
				space and str(round((float(space) / 10 ** 9), 1)) + " GB"\
					or "Unavailable")
	else:
		print __posix_unavailability

psdrive = getdrives

def eject(drive):
	"""
	Eject the cd tray whose path is the one specified.
	
	The function currently only works on Windows.
	"""
	
	if os.name == "nt":
		import executables
		subprocess.call([executables.eject, drive])
	else:
		print __posix_unavailability

