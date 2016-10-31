"""
Base convertion utility.
Bases supported are those >= 2 and <= 36

Functions:
	strbase -> strbase(number [,base, frombase]) -> string
		Converts a number from one base representation to another
		returning the result as a string.
		The range of bases supported is 2-36 inclusive.
		A number can be negative or positive
	
	getvalue -> getvalue(number [,base]) -> int
		Gets the value in base 10 of a number in the specified base.
		A number can be positive or negative.
	
	Exceptions raised by both functions are ValueError.
"""

from string import uppercase
from itertools import count

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

def getvalue(number, base=10):
	"""	int
	Gets the value in base 10 of a number in the specified base
	Any number positive or negative number unless it's a float
	
	The function is on average 10 times slower than Python's int function.
	"""
	
	if not (isinstance(base, int) or isinstance(base, long)):
		raise ValueError("Invalid value : {} entered as base of number.".format(base))
	
	if not 2 <= base <= 36:
		raise ValueError("Bases to get values from must be >=2 and <= 36.")
	
	number = str(number)
	if "." in number:
		raise ValueError("Cannot operate on floating point numbers.")
	if number.startswith("-"):
		return -getvalue(number, base)
	
	def get_ordinance_values():
		zero_ordinance = ord("0")
		a_ordinance = ord("a")
		
		for i in reversed(number.lower()):
			ordinance = ord(i)
			if ordinance - zero_ordinance < 10:
				yield ordinance - zero_ordinance
			else:
				yield 10 + (ordinance - a_ordinance)
	
	result = 0
	for v, p in itertools.izip(get_ordinance_values(), count()):
		if v < base:
			result += (v * pow(base, p))
		else:
			raise ValueError("Number : {number} is too large for base {b}".format(number = number, b = base))
	
	return result

