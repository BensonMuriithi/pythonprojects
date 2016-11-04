"""
Functions that target the shell.
"""

import tempfile
import subprocess
import os
import itertools
import chardet
import shared_content
from contextlib import contextmanager

def cls():
	"""
	Wipes all text on the shell but input history and namespace variables
	are not affected.
	"""
	from sys import version, platform
	
	os.system("cls")	
	print
	
	print "Python {pyversion} on {pyplatf}".format(
			pyversion = version, pyplatf = platform,
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
			raise TypeException(
			"Object of type {} does not have members or data to clear.".format(
					variables.__class__))
	
	for x in variables.keys():
		if not x.startswith('__') and x not in omit:
			del variables[x]
	
	if 'y' in raw_input("Clear console? (y / n) >> ").lower():
		cls()


@shared_content.assert_argument_type(str)
def start(f):
	"""
	Starts a specified file using the default set for that type of file
	If the name specified isn't an existing path but a program whose
	main process holds the name, that program is launched or launched in a new
	window if already running.
	
	arguments:
	
	f: Path of file or name of process to start. (Required)
	"""
	
	os.startfile(f)

@shared_content.Windowsonly
@shared_content.assert_argument_type(str)
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

@shared_content.Windowsonly
@shared_content.assert_argument_type(str)
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
		#will be better on a set than a list.
			
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

@contextmanager
def _getfileobject(f):
	"""
	Contextmanager helper function for cat and more.
	Gets a file object from the argument passed to cat or more and seeks to 
	the start before giving it to the funtion it is helping.
	If a file object can not be attained from the provided argument, it raises
	an IOError
	"""
	
	if isinstance(f, file):
		if f.closed:
			f = open(f.name)
	elif os.path.isfile(f):
		f = open(f)
	else:
		raise IOError("Can only read contents of files.")
	
	f.seek(0)
	yield f
	f.close()

@shared_content.assert_argument_type((str, file))
def cat(f):
	"""
	Print the contents of a file.
	
	arguments:
	
	f: File or name of file to read.  (Required)
	
	synonymns: cat, stream
	"""
	with _getfileobject(f) as ff:
		print "".join(ff)

stream = cat

@shared_content.Windowsonly
@shared_content.assert_argument_type((str, file))
def more(f):
	"""
	Print the contents of a file 10 lines at a time.
	
	arguments:
	
	f: File or name of file to read.   (Required)
	"""
	
	import msvcrt#reason for Windows only. Posix equivalent of current
	#get_morecharater will be included
	
	def get_morecharater():
		while not msvcrt.kbhit():
			pass
		
		return msvcrt.getch()
	
	with _getfileobject(f) as xfr:
		step = 40
		
		lines = 0
		for l in xfr:
			lines += 1
		
		num_of_lines = lines
		more_string_length = len("-- More -- ({}%)")
		xfr.seek(0)
		try:
			while 1:
				print "".join(itertools.islice(xfr, 0, step))
				lines -= step
				
				if lines > 0:
					print "-- More -- ({}%)".format(
						int(round((float(num_of_lines - lines) / num_of_lines) * 100))),
					
					if get_morecharater() not in (' ', '\r'):
						to_step = 2
					else:
						to_step = 25
					
					after_more = next(xfr)
					print "\r{}{}".format(after_more.rstrip("\n"),
							" "*(more_string_length -len(after_more) + 1))
					lines -= 1
				else:
					break
				step = to_step
		except KeyboardInterrupt:
			print "\r^C" + " " * (more_string_length-2)


@shared_content.Windowsonly
def shutdown():
	"""
	Shuts down the local computer.
	
	
	synonymns:  shutdown, stopcomputer
	"""
	
	subprocess.call("shutdown /p")

stopcomputer = shutdown

@shared_content.Windowsonly
def restartcomputer():
	"""
	Completely shuts down the computer then restarts it.
	
	synonymns: restartcomputer, restart
	"""
	subprocess.call("shutdown /r -t 00")


restart = restartcomputer

@shared_content.Windowsonly
def getdrives():
	"""
	Prints the info of drives connnected to the computer.
	The function currently only works on windows and utilises the wmic command
	
	
	synonymns: getdrives, psdrive
	"""
	
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
	
	format_template = "\t{0}\t\t\t   {1}\t\t  {2}"
	#result of trial and error for best fit .join() isn't flexible enough
	
	print format_template.format(*(shared_content.format_cmdoutput(f.readline())\
						for f in result_files))
	
	print "  {0}\t\t{1}\t\t{2}".format(*itertools.repeat("-"*15, len(result_files)))
	
	for i in itertools.izip(*result_files):
		name, vol_name, space = (shared_content.format_cmdoutput(s) for s in i)
		if name:
			print format_template.format(name,
				vol_name or ("(CD-ROM)" if name in shared_content.cddrives()\
							else "Unavailable"),
				space and str(round((float(space) / 10 ** 9), 1)) + " GB"\
					or "Unavailable")

psdrive = getdrives

@shared_content.Windowsonly
@shared_content.assert_argument_type(str)
def eject(drive):
	"""
	Eject the cd tray whose path is the one specified.
	
	The function currently only works on Windows.
	"""
	
	subprocess.call([shared_content.eject, drive])

