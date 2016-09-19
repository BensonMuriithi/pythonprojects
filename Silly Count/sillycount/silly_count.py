"""Integer base conversions module

Exception classes:
	class InvalidBaseError(ValueError): pass
	class FloatConvertError(ValueError): pass
	class IncorrectBaseError(ValueError): pass
"""

from math import log, ceil, floor
from collections import deque
from itertools import repeat
from string import uppercase, digits, atof
import re

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
	
	if not frombase == 10:
		number = getvalue(number, frombase)
	
	if 1 >= base or base >= len(__alphanumerals) or not floor(base) == base:
		raise InvalidBaseError("Invalid value: {} entered as base to convert to. \n{}".format(base,
			"Assert that the base to convert to is a decimal integer."))
	
	if isinstance(number, str):
		try:
			number = atof(number)
		except ValueError:
			#The first check of whether the base is 10 would have already corrected the number
			raise IncorrectBaseError("Incorrect base passed as base of number -> number: {} base: {}".format(number, frombase))
	
	if number > floor(number):
		raise FloatConvertError("The number to be converted must not be a float. {}".format(number))
	
	isNegative = False
	if number < 0:
		isNegative = True
		number = abs(number)
	
	logarithm = log(number, base) if number else 0 #get around number being zero easily
	
	ceiling = int(logarithm) + 1
	
	structure = deque(repeat(0, ceiling), maxlen = ceiling)
	
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
		structure.append(structure.popleft())
	
	return ("-" if isNegative and number else "") + reduce(lambda a, b: a + b, map(lambda a: str(a), structure))

def getvalue(number, base=10):
	"""getvalue(number [,base]) -> int
	Gets the value in base 10 of a number in the specified base
		
	Any number positive or negative number unless is a float which is not
	equivalent to its floor is accepted.
	
	All Exceptions raised by this function inherit ValueError thus it can be used
	to catch them.
	"""
	if not base == int(base):
		raise InvalidBaseError("Invalid value : {} entered as base of number. \n{}".format(base),
			"Assert that the specified base of the number is an integer.")
	
	if base >= len(__alphanumerals):
		raise InvalidBaseError("The base: {} is too large for conversion.".format(base))
	
	isNegative = False
	
	if isinstance(number, float):
		if floor(number) < number:
			raise ValueError("Invalid integer supply for conversion. Must not be float")
		else:
			isNegative = number < 0
			number = str(int(abs(number)))
	elif isinstance(number, str):
		if not number.find('.') == -1:
			if re.search(r"[.][1-9]*"): raise ValueError("Invalid integer supply for conversion. Must not be float")
			else: number = number.split('.')[0]
		
		if number.startswith(("+", "-")):
			isNegative = number[0] == '-'
			number = number[1:]
	else:
		isNegative = number < 0
		number = str(abs(int(number))) #Accomodate shorter longs ha:)
	
	number_list = None
	
	try:
		number_list = [int(i) if base <= 10 else __alphanumerals.index(i.upper()) for i in number]
		del number
		if filter (lambda a: a > base, number_list):
			raise ValueError
	except ValueError:
		raise ValueError("Invalid value : {} for base {}".format(number, base))
	
	#map function:
		#xrange is reversed so the first digit appearing in the list is multiplied
		#by the its occurence as we understand it ie
			#if the digits in number_list were 45, 4 will be multiplied by
			#the base raised by 1 instead of 0
		
	value = reduce(lambda a, b: a + b, 
		map(lambda d, p: d * (base ** p), number_list, xrange(len(number_list) - 1, -1,-1))
	)
	return -value if isNegative else value

