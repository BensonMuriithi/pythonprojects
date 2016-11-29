"""
Functions that target the shell.
"""

import os
import subprocess
try:
	from . import shared_operations
except (SystemError, ValueError):
	import shared_operations

from io import StringIO
from contextlib import contextmanager


def cls():
	"""
	Wipes all text on the shell but input history and namespace variables
	are not affected.
	"""
	from sys import platform, version
	
	subprocess.Popen(os.name == "posix" and "clear" or "cls", shell = 1)	
	print
	
	print("Python %s on %s" % (version, platform))
	print("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.")


@shared_operations.platform_check("nt")
@shared_operations.assert_argument_type(str)#accept process ids soon
def stop(process):
	""" 
	Forcefully kill a process and all its child processes.
	
	arguments:
	
	process: name of the process to kill. (Required)
	
	
	synonymns: stop, kill, stopprocess, taskkill
	"""
	
	subprocess.call("taskkill /f /t /im %s.exe" % process.replace(".exe", ""))
	

kill = stopprocess = taskkill = stop

@shared_operations.platform_check("nt")
@shared_operations.assert_argument_type(str)
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
		subprocess.call("tasklist /fi \"imagename eq {}.exe\"".format(
				process.replace(".exe", "")))
		print
		return
	
	def iterate_processes():
		"""
		Generator of lines from the call of tasklist to print.
		Skips lines whose imagename has already been printed.
		"""
		added_names = set()
		
		for l in StringIO(subprocess.check_output("tasklist")):
			exe_location = l.find(".exe")
			if exe_location != -1:
				if not l[:exe_location + 1] in added_names:
					added_names.add(l[:exe_location + 1])
					yield l
			else:
				yield l
	
	print("".join(iterate_processes()))

getprocess = tasklist

@contextmanager
def _getfileobject(f):
	"""
	Contextmanager helper function for cat and more.
	Gets a file object from the argument passed to cat or more and seeks to 
	the start before giving it to the funtion it is helping.
	If a file object can not be attained from the provided argument, it raises
	an OSError
	"""
	
	if isinstance(f, str):
		if not os.path.isfile(f):
			raise OSError("%s is not a readable file" % f)
		f = open(f)
	elif hasattr(f, "read"):
		if f.closed:
			f = open(f.name)
		if not f.readable():
			raise OSError("File provided is not opened for reading")
		f.seek(0)
	
	yield f
	
	f.close()
	

def cat(f):
	"""
	Print the contents of a file.
	
	arguments:
	
	f: File or name of file to read.  (Required)
	
	synonymns: cat, stream
	"""
	with _getfileobject(f) as ff:
		print("".join(ff))

stream = cat

@shared_operations.platform_check("nt")
def more(f):
	"""
	Print the contents of a file 10 lines at a time.
	
	arguments:
	f: File or name of file to read.   (Required)
	"""
	
	with _getfileobject(f) as file:
		terminal_height = os.get_terminal_size().lines - 4
		step = terminal_height > 0 and terminal_height or os.get_terminal_size().lines
		terminal_height = step
		more_string_length = len("-- More -- (00%)")
		no_lines = 0
		
		for l in file: no_lines+=1
		
		file.seek(0)
		linecounter = 0
		
		from itertools import islice
		from msvcrt import getch
		from sys import stdout
		
		while 1:
			print("".join(islice(file, 0, step)))
			linecounter += step
			if no_lines - linecounter < 1:
				break
			
			print "-- More -- ({:2}%)".format(
			int(round((float(linecounter) / no_lines) * 100))),
			
			stdout.flush()
			keypress = ord(getch())
			if keypress is 3:
				print
				break
			step = keypress in (32, 13) and terminal_height\
								or terminal_height >> 2 or step
			
			followmore = file.readline().rstrip("\n")
			print("\r{}{}".format(
			followmore, " " * (more_string_length - len(followmore))
			))
			
			linecounter += 1

def _shutdown_restart_abort(_wait, actionname):
	from time import sleep
	from threading import Thread, Event
	from msvcrt import kbhit, getch
	
	def countdown(action, evnt_object):
		for i in range(_wait - 2, -1, -1):
			if not evnt_object.is_set():
				print "\r{} in {:^3} seconds. Press ESC or CTRL-C to abort".format(
							action, i),
				sleep(1)
			else:
				break
	
	event = Event()
	abort_thread = Thread(target = countdown,
			name = "sysutil %s abort thread" % actionname.lower(),
			args = (actionname, event),
			daemon = True)
	
	abort_thread.start()
	
	try:
		while abort_thread.is_alive():
			if kbhit() and ord(getch()) is 27:
				raise KeyboardInterrupt
	except KeyboardInterrupt:
		event.set()
		print
		return 1
	
	return 0

@shared_operations.platform_check("nt")
def shutdown(_wait = -1):
	"""
	Shuts down the local computer after a given time in seconds.
	If a positive number is provided as an argument, a timer is
	set for the computer to shutdown and the user is provided with a
	countdown to abort the operation.
	If a negative number or no number is given for the wait time, the wait
	time used is 15 seconds
	
	arguments:
	 wait -> A number representing the period to shut down the computer after.
			If a negative number is given, the default 15 seconds is used.
	
	synonymns:  shutdown, stopcomputer
	"""
	if not _shutdown_restart_abort(_wait > -1 and _wait+1 or 16, "Shutting down"):
		subprocess.call("shutdown /p")
		return
	
	print("Shutdown aborted.")
	
stopcomputer = shutdown

@shared_operations.platform_check("nt")
def restartcomputer(_wait = -1):
	"""
	Restarts the local computer after a given time in seconds.
	
	If a positive number is provided as an argument, a timer is
	set for the computer to restart and the user is provided with a
	countdown to abort the operation.
	If a negative number or no number is given for the wait time, the wait
	time used is 15 seconds
	
	arguments:
	 wait -> A number representing the period to restart the computer after.
			If a negative number is given, the default 15 seconds is used.
	
	synonymns: restartcomputer, restart
	"""
	if not _shutdown_restart_abort(_wait > -1 and _wait + 1 or 16, "Restarting"):
		subprocess.call("shutdown /r /t 00")
		return
	
	print("Restart aborted.")

restart = restartcomputer

@shared_operations.platform_check("nt")
def getdrives():
	"""
	Prints the info of drives connnected to the computer.
	The function currently only works on windows and utilises the wmic command
	
	
	synonymns: getdrives, psdrive
	"""
	
	results = [StringIO(subprocess.check_output("wmic logicaldisk get %s" % s))\
				for s in ("name", "volumename", "freespace")]
	
	from itertools import repeat
	
	format_template = "\t{0}\t\t\t   {1}\t\t  {2}"
	
	print(format_template.format(*(next(f).strip() for f in results)))
	
	print("  {0}\t\t{1}\t\t{2}".format(*repeat("-"*15, 3)))
	
	space_str = lambda s: str(round(float(s) / 10**9, 1)) + " GB"
	strip_strs = lambda three: (s.strip() for s in three)
	
	for name, vol_name, space in (strip_strs(t) for t in zip(*results)):
		if name:
			print(format_template.format(
			name,
			vol_name or (name in shared_operations.cddrives() and "(CD-ROM)" or "Unavailable"),
			space and space_str(space) or "Unavailable"))
	

psdrive = getdrives

@shared_operations.platform_check("nt", "posix")
@shared_operations.assert_argument_type(str)
def eject(drive = ""):
	"""
	Eject the cd tray of a drive specified.
	If no drive is specified, it is checked if there is exactly one drive with
	a cd tray connected to the computer and if so that cd tray is ejected.
	
	The function currently relies on an executable and only works on Windows.
	"""
	
	if os.name == "posix":
		subprocess.call("eject")
		return
		
	if not drive:
		if len(shared_operations.cddrives()) is 1:
			drive = shared_operations.cddrives()
		else:
			print("This computer does not connected to a cd tray.")
			return
	elif not drive.replace("/", "\\").strip("\\") in shared_operations.cddrives():
		print("{} is not a drive with a cd tray.".format(drive))
		return
	
	subprocess.call([shared_operations.eject, drive])

