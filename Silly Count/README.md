Convert numbers to and from different bases.

sillycount contains two functions:

sillycount.getbase(number [,to_base, from_base]) -> converts the number 'number' from its
	specified base 'from_base' which defaults to 10, to the base 'to_base' which
	by default is 2

sillycount.getvalue(number [,base]) -> gets the base 10 value of number without drectly
	calling int(str). I've tested it and accuracy is great and performance is better
	then expected.
