from effects import ellipsis
from effects import wait
from scene import Scene
from random import randint

class EscapePod(Scene):
	def introduce(self):
		ellipsis(4)
		wait(0.88)
		
		print "You enter the escape pod and attempt to initialise it."
		
		wait(1.3)
		
		print "The pod has an unlock key which is one digit."
		print "You have to guess the digit within five attempts or the pod won't start."
		
		wait(1.5)
		self.__guess()
		
	def __guess(self):
		"This stage is included to add a bit more thrill and excitement to the game"
		number = randint(1, 9)
		num_of_guesses = 0
		
		while num_of_guesses < 5:
			if num_of_guesses > 0: print "\nTry again."
			trial = int(raw_input("Enter start number > "))
			num_of_guesses += 1
			if trial == number:
				self.__finish()
			
		self.__die_here()
			
	def __finish(self):
		wait(0.5)
		print "Correct!\n"
		wait(0.77)
		print "The pod starts and takes off heading to the planet."
		wait(0.7)
		if self.engine.bomb_set: 
			print "KABOOM!!\nThe ships blows up behind you."
			wait(0.4)
			
		print "Good job!"
		
		ellipsis(4)
		wait(3)
		print "\n\tGoodbye!"
		wait(1.5)
		exit(0)
		
	def __die_here(self):
		wait(0.5)
		print "Incorrect!"
		
		ellipsis(4)
		wait(0.55)
		if self.engine.bomb_set: print "\nKABOOOM!!\nThe ship along with the escae pod blows up."
		else: print "The gothon tail pierces through the pod's door and stabs you right in the back."
		self.engine.death()