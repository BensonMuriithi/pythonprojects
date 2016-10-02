"""
This module converts a number from one base to another.
Bases supported must be >= 2 and <= 36
"""

from string import uppercase

__dig_to_chr = lambda num: str(num) if num < 10 else uppercase[num - 10]

def strbase(number, base = 2, frombase = 10):
	"""strbase -> strbase(number [,base, frombase]) -> string
			Converts a number from one base representation to another
			returning the result as a string.
			The range of bases supported is 2-36 inclusive.
			A number can be negative or positive
			Specify the base to convert from as the third argument or
			woth the keyword frombase if it isn't 10.
	"""
	
	#credit for this function goes to "random guy" on stack overflow
	#http://stackoverflow.com/questions/2063425/python-elegant-inverse-function-of-intstring-base
	
	#http://stackoverflow.com/users/196185/random-guy
	
	if not 2 <= base <= 36:
		raise ValueError("Base to convert to must be >= 2 and <= 36")
	
	if frombase != 10:
		number = int(number, frombase)
	
	if number < 0:
		return "-" + strbase(-number, base)
	
	d, m = divmod(number, base)
	if d:
		return strbase(d, base) + __dig_to_chr(m)
	
	return __dig_to_chr(m)

