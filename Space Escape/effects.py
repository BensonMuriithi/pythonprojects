from time import sleep

def ellipsis(x):
	for i in range(0, x):
		sleep(0.35)
		print ".",
		
	print "\n"
		
def wait(x):
	sleep(x)