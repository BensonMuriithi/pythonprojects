from math import log

def get_checkbits(m):
	return int(log(m, 2)) + 1

