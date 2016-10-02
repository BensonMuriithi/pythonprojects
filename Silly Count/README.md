Convert numbers to and from different bases.

Functions to use in sillycount are:

sillycount.strbase.strbase(number [,base] [,frombase]) -> Converts a number from
	one base to another.

sillycount.silly_count.getvalue(number [,base]) -> gets the base 10 value of number without drectly
	calling int(str). I've tested it and accuracy is great and performance is better
	then expected.
