"""
Functions that target the shell.
"""

import tempfile
import subprocess
import os

__python_text = "Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:24:40) \
[MSC v.1500 64 bit (AMD64)] on win32\n\
Type \"help\", \"copyright\", \"credits\" or \"license\" for more information."
#Could not find a way to programmatically fetch this text directly from the installed python.


def cls():
	"""
	cls -> wipes all text on the shell but input history and namespace variables
	are not affected.
	"""
	os.system("cls")
	print "\n" + __python_text

def start(f):
	"""start(filename) -> starts a specified file using the default set for that type of file
	If the name specified isn't an existing path but a program whose
	main process holds the name, that program is launched or launched in a new
	window if already running.
	"""
	
	os.startfile(f)

def stop(process):
	"""stopprocess(process) / kill / stop / taskkill -> 
	Forcefully kill a running process and all itschild processes.
	"""
	
	outputfile = tempfile.TemporaryFile()
	
	result = subprocess.call("taskkill /f /t /im".split() + ["{}.exe".format(process)],
		stdout = outputfile, stderr = outputfile)
	
	if result != 0:
		print "Kill of {}.exe unsuccessful.".format(process)

kill = stopprocess = taskkill = stop

def tasklist(process = ""):
	"""
	getprocess(process = "") / tasklist -> Get the list of running processes. 
	To simulate omitting child processes, a process name will be printed only once.
	
	If a specific task name is provided, the task(s) whose name match it are listed. 
	"""
	
	if process:
		subprocess.call("tasklist /fi \"imagename eq {}.exe\"".format(process))
		print
		return
	
	f = tempfile.TemporaryFile(bufsize = 0)
	subprocess.call("tasklist", bufsize = 0, stdout = f, stderr = f)
	
	f.seek(0)
	lines = []
		
	for l in f:
		exe_location = l.find(".exe")
		
		if exe_location != -1:
			if not [0 for n in lines[::-1] if n[:exe_location] == l[:exe_location]]:
				#no need to +1
				#start from end as it's more likely for similar name to appear
				#in close succession.
				
				lines.append(l)
		else:
			lines.append(l)
		
	print "".join(lines)

getprocess = tasklist

