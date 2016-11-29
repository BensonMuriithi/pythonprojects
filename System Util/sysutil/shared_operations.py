"""
Functions and data shared by multiple modules of sysutil
"""

import os
import glob

from io import StringIO
from functools import wraps
from subprocess import check_output

eject = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
			"executables\\eject.exe")
recycle = os.path.join(os.path.dirname(os.path.abspath(__file__)),
			"executables\\recycle.exe")
_cddrives = None

def catch_interrupt(f):
	""""
	Catches KeyboardInterrupt for functions that could take too long
	"""
	@wraps(f)
	def deco(*args, **kwargs):
		try:
			f(*args, **kwargs)
		except KeyboardInterrupt:
			print "^C"
	
	return deco

def resolve_path(s):
	drive, sub_path = os.path.splitdrive(s)
	
	return glob.iglob(drive + "".join((
		c.isalpha() and "[%s%s]" % (c.upper(), c.lower()) or\
		c for c in sub_path)))

def stat_accessible(p):
	try:
		return p, os.stat(p)
	except (OSError, IOError):
		return

def platform_check(*args):
	"""Decorate functions that require Windows"""
	
	platforms = args or ("nt", "posix")
	
	def actualdeco(f):
		@wraps(f)
		def os_check_deco(*args, **kwargs):
			if os.name in platforms:
				return f(*args, **kwargs)
			else:
				print "This operation currently does not work on %s systems" % os.name
				print "Check the source code in {}.py for more information.".format(
					os.path.abspath(f.__module__))
				
				return None
		
		return os_check_deco
	
	return actualdeco


def assert_argument_type(expect = str, **specific):
	
	def _raise(e = ""):
		raise TypeError(
		"Argument for type to expect must be a type, or tuple of types.\nProvided", e)
	
	def check_type_type(_type):
		if isinstance(_type, type):
			pass
		elif isinstance(_type, tuple):
			for t in _type:
				if not isinstance(t, type):
					_raise("({}  {})".format(type(t).__name__, t))
		else:
			_raise("{}  ({})".format(type(_type).__name__, _type))
		
	check_type_type(expect)
	for x in specific.values():
		check_type_type(x)
	
	if isinstance(expect, type):
		type_failed = expect.__name__
	else:
		type_failed = "any of ({})".format(", ".join((t.__name__ for t in expect)))
	
	def true_asserter(f):
		@wraps(f)
		def arg_type_deco(*args, **kwargs):
			for i in args:
				if not isinstance(i, expect):
					raise TypeError("{0} argument expected. {1} provided"\
									.format(type_failed, type(i).__name__))
			
			
			for name, value in kwargs.items():
				if name in specific:
					if not isinstance(value, specific[name]):
						
						failed_types = specific[name].__name__ if \
							isinstance(specific[name], type) else \
							"any of ({})".format(", ".join(tp.__name__ for tp in specific[name]))
						
						raise TypeError("Expected {0} argument for {1}. {2} provided."
									.format(failed_types, name, type(value).__name__))
				else:
					if not isinstance(value, expect):
						raise TypeError("{0} argument expected. {1} provided"\
										.format(type_failed, type(i).__name__))
			
			return f(*args, **kwargs)
		
		return arg_type_deco
	return true_asserter

def cddrives():
	"""
	Gets the drives that are cd-roms using the wmic command on cmd
	"""
	global _cddrives
	if _cddrives is None:
		_cddrives = {i for i in check_output("wmic cdrom get drive").strip().split()\
				if ':' in i}
	
	return _cddrives

