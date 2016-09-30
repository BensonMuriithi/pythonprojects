from time import time
	
def timeit(func):
	"""Decorator function to time execution of a function."""
	def wrap(*args, **kwargs):
		start = time()
		func(*args, **kwargs)
		stop = time()
		return "Function {} took {}".format(func.__name__, str((stop-start)))
	
	return wrap