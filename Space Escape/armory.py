from effects import *
from scene import Scene

class Armory(Scene):
	def introduce(self):
		ellipsis(4)
		wait(1)
		
		print "You enter the armory."
		print "There are several weapons stored here."
		wait(1)
		print "You can use them to protect yourself in case you need to.\n"
		
		wait(0.5)
		
		inv = raw_input("Enter 'Q' on the control desk to get the inventory. > ").lower()
		
		if 'q' in inv: self.__weapon_choice()
		else: self.__screams()
		
	def __weapon_choice(self):
		print """
		\r\t1: Portable Time Bomb
		\r\t2: Plama Gun Ammunition
		\r\t3: Tesla Shot Gun
		\r\t4: Flamethrower"""
		
		wait(2)
		print "\nYou can only however pick only two items."
		print "Remember also that the gothon you left could come after you so pick quickly."
		
		first_item = int(raw_input("\nEnter number of your first choice: "))
		second_item = int(raw_input("\nEnter number of your second choice: "))
		
		for i in first_item, second_item:
			if i == 1: self.engine.has_timebomb = True
			elif i == 2 and self.engine.has_plasmagun: pass
			elif i == 3: self.engine.has_teslagun = True
			elif i == 4: self.engine.has_flamethrower = True
			
		self.__screams()
		
	def __screams(self):
		ellipsis(4)
		
		print """
		\rScreech~~
		\rA terrible screeching sound is coming from the central corridor."""
		wait(0.7)
		print "It could be the gothon."
		
		wait(1)
		print "You should get out of here and head for the bridge."
		
		raw_input(" >> ")
		self.engine.bridge()