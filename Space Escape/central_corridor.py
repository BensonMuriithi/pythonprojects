from effects import *
from scene import Scene

class CentralCorridor(Scene):
	def introduce(self):
		ellipsis(5)
		print "You enter the central corridor."
		print "It connects the control room, the armory and the bridge to the escape pods."
	
		wait(1)
		print "A gothon appears on the opposite end of the corridor coming from the bridge."
		wait(1)
		self.__action()
		
	def __action(self):
		print "\nWhat do you do?\n"
		
		if self.engine.has_plasmagun: print "Shoot the gothon."
		print "Get into the armory."
		print "Try to circumvent the gothon."
		
		action = raw_input("> ").lower()
		
		if ("shoot" in action or "plasma" in action or "gun" in action or "sho" in action) and self.engine.has_plasmagun:
			self.__encourage()
		elif "in" in action or "armory" in action:
			self.engine.armory()
		else:
			self.__die()
			
	def __encourage(self):
		wait(1)
		print "\nThe gothon falls to the ground thrashing."
		wait(1)
		print "It doesn't look dead."
		wait(1)
		print "You should turn into the armory and get to the bridge from there."
		
		wait(0.7)
		action = raw_input("\nDo you? > ").lower()
		if "ye" in action or "armory" in action or "turn" in action:
			self.engine.armory()
		else:
			self.__die()
			
	def __die(self):
		wait(1)
		print "\nThe gothon jumps quickly and decapitates you with its tail."
		wait(0.5)
		self.engine.death()