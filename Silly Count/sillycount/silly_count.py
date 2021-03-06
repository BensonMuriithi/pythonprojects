"""Integer base conversions module

Exception classes:
	class InvalidBaseError(ValueError): pass
	class FloatConvertError(ValueError): pass
	class IncorrectBaseError(ValueError): pass
"""

from math import log, ceil, floor
from collections import deque
from string import uppercase, digits, atof
import itertools

__alphanumerals = (digits + uppercase)

class InvalidBaseError(ValueError): pass
class FloatConvertError(ValueError): pass
class IncorrectBaseError(ValueError): pass

def getbase(number, base=2, frombase = 10):
	"""getbase(number [,base, frombase]) -> string
	Converts a non-float number from any valid base to any other that's not greater than 36
	
	The function utilizes alphanumerals as expected.
	Valid bases to convert to or from must be greater than 1 but not greater than 36
	
	Negative number are supported as equally as positive numbers.
	
	The function raises a InvalidBaseError for invalid bases and a FloatConvertError for 
	floating point numbers
	
	Both Exceptions inherit ValueError so it can be used to cath them.
	
	The result is returned as a string of the value to accomodate bases above 10
	One can call int(v) or getvalue(v) to get the value as an integer (if it's base is <= 10)
		->getvalue is a function in this module that get the base 10(default) value
			of an Integer in as string
	"""
	
	#This function has been relegated in favour of strbase.strbase
	
	if isinstance(number, float):
		raise FloatConvertError("The number to be converted must not be a float. {}".format(number))
		
	if not frombase == 10:
		number = getvalue(number, frombase)
	
	if 1 >= base or base >= len(__alphanumerals):
		raise InvalidBaseError("Invalid value: {} entered as base to convert to. \n{}".format(base,
			"Assert that the base to convert to is a decimal integer."))
	
	if isinstance(number, str):
		try:
			number = getvalue(number)
		except ValueError:
			#The first check of whether the base is 10 would have already corrected the number
			raise IncorrectBaseError("Incorrect base passed as base of number -> number: {} base: {}".format(number, frombase))
	
	isNegative = False
	if number < 0:
		isNegative = True
		number = abs(number)
	
	logarithm = log(number, base) if number else 0 #get around number being zero easily
	
	ceiling = int(logarithm) + 1
	
	structure = deque(itertools.repeat(0, ceiling), maxlen = ceiling)
	
	while number:
		if number >= (base ** int(logarithm)):
			acceptable_digit = int(number / (base ** floor(logarithm)))
			structure.append(acceptable_digit if acceptable_digit < 10 else __alphanumerals[acceptable_digit])
			number -= acceptable_digit * (base ** floor(logarithm))
		else:
			structure.append(0)
		
		logarithm -= 1
	
	while structure[0] == 0:
		#the result needs trailing zeros
		structure.rotate(-1)
	
	return ("-" if isNegative and number else "") + reduce(lambda a, b: a + b, map(lambda a: str(a), structure))

