from effects import wait
from scene import Scene
from random import randint

class Death(Scene):
	messages = [
		"You kinda suck at this.",
		"Your mom would be proud...if she were smarter.",
		"Such a luser.",
		"I have a puppy that's better than this."]
	def enter(self):
		print "\nYou died. " + Death.messages[randint(0, len(Death.messages) - 1)]
		wait(2)
		print "\n\tGoodbye!"
		wait(1.5)
		exit(0)