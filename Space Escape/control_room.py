from effects import *
from scene import Scene

class ControlRoom(Scene):
	def introduce(self):
		print "\n\tBeeep!  Beeep!"
		print "The ship's alarm system is blaring."
		wait(1)
		print "Something is terribly wrong!"
		
		wait(2)
		print "Swish!"
		print "The control room's doors open without command."
		
		wait(1)
		print "The centre control desk is running wild with fault notifications"
		
		wait(0.8)
		print "The screens reveal that the lock and communication systems are down."
		
		wait(1.5)
		print "\nFootage from thermal seeking cameras appears on the overhead screen."
		print "A cold structure is moving swiftly through the ship's systems corridors."
		
		wait(1.34)
		print "\nYou should really leave the ship.\nThere are escape pods on the other side of the ship that can get you to the planet below."
		self.__action()
		
	def __action(self):
		print "\nWhat do you do%s?\n" % (" now" if self.engine.has_plasmagun else "")
		
		print "%sRun to the pod." % ("" if self.engine.has_plasmagun else "Get plasma gun from under the desk\n")
		
		action = raw_input("> ").lower()
		
		if "gun" in action or "plasma" in action or "desk" in action:
			self.engine.has_plasmagun = True
			self.__action()
		elif "run" in action or "rn" in action or "pod" in action or "to" in action:
			self.engine.central_corridor()
		else:
			self.__action()