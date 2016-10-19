"""
Functions and data shared by multiple modules of sysutil
"""
from functools import wraps
import os
from sys import platform
from threading import BoundedSemaphore

#paths to executables recycle and eject
eject = os.path.join(os.path.dirname(os.path.abspath(__file__)), "executables\\eject.exe")
recycle = os.path.join(os.path.dirname(os.path.abspath(__file__)), "executables\\recycle.exe")

def Windowsonly(f):
	"""Decorate functions that require Windows"""
	@wraps(f)
	def os_check_deco(*args, **kwargs):
		if platform.startswith("win"):
			return f(*args, **kwargs)
		else:
			print "This operation currently does not work on", platform
			print "Check the source code in {}.py for more information.".format(
				os.path.abspath(f.__module__))
			
			return None
	
	return os_check_deco


def assert_argument_type(expect = str, **specific):
	"""
	Function decorator that checks that the arguments provided to a function
	are of a certain type or of any type among several
	When several types are provided to crosscheck arguments against, these
	types must be in a tuple.
	
	If specific types are desired for specific keyword arguments, the
	name of the argument and its desired type should be provided as a key value
	pair ie arg_name = arg_type.
	When types are specified for specific arguments, these arguments must be 
	provided as keyword arguments when calling the function for them to be evaluated.
	
	A range of types can also be specified for a keyword argument where
	the range of types is a tuple of types.
	
	Type ranges must only be in tuples and not any other type of collection.
	"""
	
	bound_semaphore = BoundedSemaphore(1)
	
	def _raise(e = ""):
		raise TypeError("Argument for type to expect must be a type, or \
tuple of types. Provided", e)
	
	def check_type_types(*_types):
		for t in _types:
			if isinstance(t, type):
				continue
			elif isinstance(t, tuple):
				if bound_semaphore.acquire(0):#maintain a maximum 1 level of recursion
					#if a tuple was to contain other tuples instead of only types,
					#the call to acquire will return False preventing another recursion
					#and raise the TypeError
					check_type_types(*t)
					bound_semaphore.release()
				else:
					_raise(t)
			else:
				_raise(t)
	
	check_type_types(expect)
	for x in specific.itervalues():
		check_type_types(x)
	
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
			
			
			for name, value in kwargs.iteritems():
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


