from re import compile as _compile

class InvalidRoman(ValueError): pass
class NegativeNumberError(ValueError): pass

__table = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'I': 1, 'V': 5}

def __assess(parts):
	"""Evaluate the values held in every portion of the Roman number as provided by the groups from getint
		The change function returns a list of the value of each symbol in a group 's'
		The change function works as follows: 
		  If a group's length is two - the whole number is divided into groups for tens, thousands etc -, 
		  it's possible that the number is such a number as IX or CM.
		  Therefore if it's length is two and the value of the first symbol eg 'C' is less than that of the second eg 'M' - ('CM')
		  the list formed consists of the negative value of the first symbol and the true value of the second symbol
		  as per the __table dictionary
		  
		  Otherwise if the group's length is three or is two but the value of the first symbol is greater than the second,
		  the list formed holds the values of each symbol as per __table
		 
		The reduce function in turn reduces the values of the return values of change when supplied a group
		but skips empty groups.
	"""
	plus = lambda a, b: a + b
	change = lambda s: [__table[c] for c in s] if not (len(s) == 2 and __table[s[0]] < __table[s[1]]) else [-(__table[s[0]]), __table[s[1]]]
	return reduce(plus, [reduce(plus, change(s)) for s in parts if s])

def getint(rome):
	"""Accepts a Roman number in string format and returns an integer hoding the value it represents
		
		The regex search checks in portions if a part of the string is can be a Roman number
		The organization of the math groups also checks for the plausability of the number
		in that a Roman code for hundreds does not come after that of tens.
		
		This above is achieved by checking for thousands, hundreds, tens and then ones in order.
		
		The program idea was obtained from Mark Pilgrim's "Dive Into Python" book but
		has been tweaked just a bit for re-usability and effectiveness.
		
		The Exception arguments especially for those raised after assessment of the "offender" argument
		describe concisely what the probem with the provided Roman number is.
	"""
	match = _compile(r"^\s*(M{,})(CM|CD|D?C{,})(XC|XL|L?X{,})(IX|IV|V?I{,})\s*$").search(rome.upper())
	
	if not match:
		raise InvalidRoman("{} is not a valid Roman number.".format(rome))
	
	offender = filter(lambda y: len(y) > 3, match.groups())
	if offender:
		if 'M' in offender[0]:
			raise InvalidRoman("{} is not a supported Roman number".format(rome))
			#just to clarify that only numbers below 4000 are supported thus that is the error.
			
		else: raise InvalidRoman("{} is not a valid Roman number.".format(rome))
	
	return __assess(match.groups())

def getroman(number):
	"""Return the Roman number representation of an number
		If the number provided is non-negative, it is rounded and a string
		holding it's Roman representation is returned
		
		If the number provided is negative, an exception is raised.
		
		The program doesn't yet support numbers above 3999 therefore if any number greater
		is provided, the function returns None
	"""
	if number >= 4000:
		return None
	
	if number < 0:
		raise NegativeNumberError("A Roman number cannot be negative")
	
	number = int(round(number))
	roman_str = ""
	
	bounds = zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
		("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"))
	
	for i, v in bounds:
		while number >= i:
			roman_str += v
			number -= i
	
	return roman_str

