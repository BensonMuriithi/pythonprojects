"""
Custom module for measuring the execution time of a function.
Import the 'timeit' decorator which when used will execute the decorated 
function and measure the time taken for that function to complete.

The result is formatted into a string and returned to be printed or logged.
"""

from time import time
	
def timeit(func):
	"""Decorator function to time execution of a function."""
	def wrap(*args, **kwargs):
		start = time()
		func(*args, **kwargs)
		stop = time()
		return "Function {} took {}".format(func.__name__, str((stop-start)))
	
	return wrap

