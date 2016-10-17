"""
Functions and data shared by multiple modules of sysutil
"""
from functools import wraps
import os

def Windowsonly(f):
	"""Decorate functions that requires Windows"""
	@wraps(f)
	def deco(*args, **kwargs):
		if os.name == "nt":
			return f(*args, **kwargs)
		else:
			print "Until this functionality is added to the package for other \
				platforms by Benson Muriithi \nkindly add it yourself if you can."
			return None
	
	return deco

#paths to executables recycle and eject
eject = os.path.join(os.path.dirname(os.path.abspath(__file__)), "executables\\eject.exe")
recycle = os.path.join(os.path.dirname(os.path.abspath(__file__)), "executables\\recycle.exe")
