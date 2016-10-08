from effects import wait
from effects import ellipsis
from scene import Scene
from random import randint

class Bridge(Scene):
	def introduce(self):
		ellipsis(5)
		wait(0.8)
		
		print "You get to the bridge and continue runnning towards the pods."
		wait(0.89)
		
		print "The gothon enters the bridge behind you."
		wait(1)
		print "It's coming after you."
		
		self.__fight()
		
	def __fight(self):
		print "\nWhat do you do?\n"
		
		if self.engine.has_flamethrower: print "Fire the flamethrower at the gothon."
		if self.engine.has_plasmagun: print "Shoot gothon with plasma gun."
		if self.engine.has_teslagun: print "Shoot gothon with tesla gun."
		print "Challenge the gothon to a stare down contest."
		
		action = raw_input("> ").lower()
		
		if ("fire" in action or "flame" in action) and self.engine.has_flamethrower:
			print "The gothon catches fire and falls to the ground wrigling."
			self.__bombset()
		elif ("shoot" in action or "fire" in action or "gun" in action) and self.engine.has_gun():
			print "The gothon is subdued but only temporarily."
			self.__bombset()
		elif "stare" in action or "down" in action or "chal" in action:
			ellipsis(2)
			print "Oh God!\nThe creature doesn't even have eyes!"
			self.__die_here()
		else:
			self.__die_here()
			
	def __die_here(self):
		ellipsis(2)
		print "\nThe gothon leaps and swings its tail decapitating you."
		self.engine.death()
		
	def __bombset(self):
		if self.engine.has_timebomb:
			ellipsis(5)
			print "\nProtocol dictates that if a breach such as this one occurs a ship be destroyed."
			print "You should set the time bomb to explode as you escape to the planet."
			
			wait(1.11)
			action = raw_input("\nDo you? > ").lower()
			if "ye" in action:
				wait(1.1)
				print "The bomb is set."
				self.engine.bomb_set = True
			
		
		self.__pod_choice()
		
	def __pod_choice(self):
		ellipsis(4)
		print "You get to a point where the bridge splits to two other bridges."
		print "Oh! Yes. One of the pods is disfunctional due to some faults."
		print "You will have to guess which of the routes leads to the functional pod.\n"
		
		wait(1.2)
		print "Which route will you take, left or right?\n"
		
		correct = randint(1, 2)
		route = raw_input("> ").lower()
		if "le" in route:
			self.__right_choice() if correct == 1 else self.__wrong_choice()
		elif "ri" in route:
			self.__right_choice() if correct == 2 else self.__wrong_choice()
		else:
			self.__wrong_choice()
			
	def __right_choice(self):
		wait(2)
		
		print "Good job! This is the functional escape pod."
		print "Get into the pod quickly %s" % ("or you'll blow up together with the ship." if self.engine.bomb_set else "before the gothon catches up with you.")
		
		raw_input(" >> ")
		self.engine.escape_pod()
		
	def __wrong_choice(self):
		wait(2)
		
		print "Oh, God! This is the non-functioning pod."
		print "\nScreeech~~"
		print "The gothon!"
		
		ellipsis(4)
		self.engine.death()