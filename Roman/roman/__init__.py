"""
Evaluates and converts Roman numbers to integers and vice versa.
The functions only support Roman numbers below 4000 for conversions.
"""

from re import compile as _compile

class InvalidRoman(ValueError): pass
class OutofBoundError(ValueError):	pass

table = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'I': 1, 'V': 5}
compiled_pattern = _compile(r"\s*(M{,3})(CM|CD|D?C{,3})(XC|XL|L?X{,3})(IX|IV|V?I{,3})\s*$")

def getint(roman_str):
	"""
	Accepts a Roman number as a string and returns an integer
	of the value it represents
	"""
	
	match = compiled_pattern.match(roman_str.upper())
	
	if not match:
		raise InvalidRoman("{} is not a valid Roman number.".format(roman_str.strip()))
	
	def convert_bit(s):
		return (len(s) is 2 and table[s[1]] > table[s[0]]) and \
				(table[s[1]] - table[s[0]],) or (table[i] for i in s)
	
	from functools import reduce
	from operator import add
	
	return reduce(add, (reduce(add, convert_bit(s)) for s in match.groups() if s))

def getroman(number):
	"""
	Return the Roman number representation of an number
	If the number provided is non-negative, it is rounded and a string
	holding it's Roman representation is returned
	
	If the number provided is negative, an exception is raised.
	
	The program doesn't yet support numbers above 3999 therefore if any number greater
	is provided, the function returns None
	"""
	if not 0 < number < 4000:
		raise OutofBoundError("roman supports numbers > 0 and < 4000")
	
	if not isinstance(number, int):
		raise ValueError("Roman numbers can only be positive integers")
	
	roman_str = ""
	
	bounds = zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
		("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"))
	
	for i, v in bounds:
		while number >= i:
			roman_str += v
			number -= i
	
	return roman_str

