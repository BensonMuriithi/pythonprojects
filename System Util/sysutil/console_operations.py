"""
Functions that target the shell.
"""

import tempfile
import subprocess
import os
import itertools
import chardet
import io
import threading
from contextlib import contextmanager
from sys import platform, version

if platform.startswith("win"):
	import msvcrt

try:
	from . import shared_content
except SystemError:
	import shared_content

def cls():
	"""
	Wipes all text on the shell but input history and namespace variables
	are not affected.
	"""
	os.system("cls")	
	print()
	
	print("Python %s on %s" % (version, platform))
	print("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.")


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
	
	outputfile = tempfile.TemporaryFile(buffering = 1)
	
	process = process.rstrip(".exe")
	result = subprocess.call("taskkill /f /t /im %s.exe" % process,
		stdout = outputfile, stderr = outputfile)
	
	if result != 0:
		outputfile.seek(0)
		print(outputfile.read())

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
		subprocess.call("tasklist /fi \"imagename eq %s.exe\"" % process.rstrip(".exe"))
		print()
		return
	
	def iterate_processes():
		"""
		Generator of lines from the call of tasklist to print.
		Skips lines whose imagename has already been printed.
		"""
		f = tempfile.TemporaryFile(mode='r+',buffering=1)
		subprocess.call("tasklist", bufsize = 0, stdout = f, stderr = f)
		f.flush()
		
		f.seek(0)
		added_names = set()
		for l in f:
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
	an IOError
	"""
	
	if isinstance(f, file):
		if f.closed:
			f = open(f.name)
	elif os.path.isfile(f):
		f = open(f)
	else:
		raise OSError("Can only read contents of files.")
	
	f.seek(0)
	yield f
	f.close()

@shared_content.assert_argument_type((str, io.TextIOWrapper, io.StringIO))
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

@shared_content.Windowsonly
@shared_content.assert_argument_type((str, io.TextIOWrapper, io.StringIO))
def more(f):
	"""
	Print the contents of a file 10 lines at a time.
	
	arguments:
	
	f: File or name of file to read.   (Required)
	"""
	
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
				print("".join(itertools.islice(xfr, 0, step)))
				lines -= step
				
				if lines > 0:
					print("-- More -- ({}%)".format(
						int(round((float(num_of_lines - lines) / num_of_lines) * 100))),
						end=' ')
					
					if get_morecharater() in (' ', '\r'):
						to_step = 25
					else:
						to_step = 2
					
					after_more = next(xfr)
					print("\r{}{}".format(after_more.rstrip("\n"),
							" "*(more_string_length -len(after_more) + 1)))
					lines -= 1
				else:
					break
				step = to_step
		except KeyboardInterrupt:
			print("\r^C" + " " * (more_string_length-2))


def _shutdown_restart_abort(_wait, actionname):
	from time import sleep
	def countdown(action, evnt_object):
		for i in range(_wait - 2, -1, -1):
			if not evnt_object.is_set():
				print("\r{} in {:^3} seconds. Press ESC or CTRL-C to abort".format(
							action, i), end = "")
				sleep(1)
			else:
				break
	
	event = threading.Event()
	abort_thread = threading.Thread(target = countdown,
			name = "sysutil %s abort thread" % actionname.lower(),
			args = (actionname, event),
			daemon = True)
	
	abort_thread.start()
	
	try:
		while abort_thread.is_alive():
			if msvcrt.kbhit() and ord(msvcrt.getch()) is 27:
				raise KeyboardInterrupt
	except KeyboardInterrupt:
		event.set()
		print()
		return 1
	
	return 0

@shared_content.Windowsonly
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

@shared_content.Windowsonly
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

@shared_content.Windowsonly
def getdrives():
	"""
	Prints the info of drives connnected to the computer.
	The function currently only works on windows and utilises the wmic command
	
	
	synonymns: getdrives, psdrive
	"""
	
	namefile = tempfile.TemporaryFile(buffering = 1)
	volumenamefile = tempfile.TemporaryFile(buffering = 1)
	freespacefile = tempfile.TemporaryFile(buffering = 1)
	
	#Store the result of each detail for later formatting.
	subprocess.call("wmic logicaldisk get name", stdout = namefile)
	subprocess.call("wmic logicaldisk get volumename", stdout = volumenamefile)
	subprocess.call("wmic logicaldisk get freespace", stdout = freespacefile)
	
	result_files = (namefile, volumenamefile, freespacefile)#no performance hit
	for f in result_files:
		f.seek(0)
	
	format_template = "\t{0}\t\t\t   {1}\t\t  {2}"
	#result of trial and error for best fit .join() isn't flexible enough
	
	print(format_template.format(*(shared_content.format_cmdoutput(f.readline())\
						for f in result_files)))
	
	print("  {0}\t\t{1}\t\t{2}".format(*itertools.repeat("-"*15, len(result_files))))
	
	for i in zip(*result_files):
		name, vol_name, space = (shared_content.format_cmdoutput(s) for s in i)
		if name:
			print(format_template.format(name,
				vol_name or ("(CD-ROM)" if name in shared_content.cddrives()\
							else "Unavailable"),
				space and str(round((float(space) / 10 ** 9), 1)) + " GB"\
					or "Unavailable"))

psdrive = getdrives

@shared_content.Windowsonly
@shared_content.assert_argument_type(str)
def eject(drive = ""):
	"""
	Eject the cd tray of a drive specified.
	If no drive is specified, it is checked if there is exactly one drive with
	a cd tray connected to the computer and if so that cd tray is ejected.
	
	The function currently relies on an executable and only works on Windows.
	"""
	
	if not drive:
		if len(shared_content.cddrives()) is 1:
			drive = shared_content.cddrives()
		else:
			print("This computer does not connected to a cd tray.")
			return
	elif not drive in shared_content.cddrives():
		print("{} is not a drive with a cd tray.".format(drive))
		return
	
	subprocess.call([shared_content.eject, drive])

