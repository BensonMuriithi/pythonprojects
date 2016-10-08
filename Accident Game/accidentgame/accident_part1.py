"""first part of code of bens_accident game
contains scenes of the player coming around and availing the player an opportunity
to call the police or an ambulance
"""
from time import sleep
from accident_part2 import call_of_help

def come_around():
	"""The game's starting point where the persona regains consiousness"""
	print "\"Oooh! Aaarh!\""
	sleep(1.5)
	print """
	\rYou are coming around in a spinning haze not knowing what's going on.
	\rAs your senses come back to you, you hear an incessant ringing noise.
	\rYou also make out water falling and a cracked up view.
	\rYou start feeling some stress in a lower part of you but you dont't know what it is.
	\rThe ringing noise is getting weaker
	\rYou feel a headache and immediately realise that something heavy is lying on your knees.
	"""
	check_on_knees()
	
def check_on_knees():
	"""player is presented with chance to learn what is causing the character stress in his legs"""
	print "What do you do at this point?"
	action1 = raw_input("> ").lower()
	if "look" in action1 and "down" in action1 or "check" in action1:
		look_down()
	elif "down" in action1 or "knee" in action1 or "leg" in action1 or "lift" in action1:
		look_down()
	else:
		look_around(False)
		
def look_down():
	print "You try to bend a little and look at what is causing the discomfort in you legs."
	print "Argh!"
	print """A seat belt holds you back and you feel a sharp pain in your right shoulder.
	\rWhat do you do?
	"""
	
	belt_off = raw_input("> ").lower()
	if "off" in belt_off:
		print "You take the belt off and look down to your knee."
		print "It appears to be caught under the dash board."
		print "You try to lift it off but you it's too heavy and you leave it."
		look_around(False)
	else:
		print "The pain in your shoulder jolts you and makes you bend your knee."
		print "\n\"AAAARRRGH!!\"\nThe pain is unbearable."
		look_around(True)
		
def look_around(is_hurt):
	print """
	\rYou look around the vehicle and the sights rekindle your memory.
	\rYou were driving home from your company."""
	sleep(4)
	print"""It takes a second for you to remember how exactly your car crashed
	\rYou were driving up a hill and it was raining cats and dogs you remember.
	\rYes; some vehicle blinded you with its headlights as it
	\rcame down from the hill's summit to which you were close.
	\rThe vehicle swerved and collided with your car head on.
	\rThe rest you remember is.. waking up in dizziness
	"""
	print "You remember you had your phone in your blazer's front pocket."
	get_phone = raw_input("Do you reach for it? > ").lower()
	if "yes" in get_phone or "get" in get_phone or "yeah" in get_phone:
		use_phone(is_hurt)
	else:
		fumble(is_hurt, False)
		
def use_phone(is_hurt):
	if(is_hurt): print "\"Ouch!\" The shoulder is hurting."
	
	print "\nWhat do you want to do with the phone?"
	phone_action1 = raw_input("> ").lower()
	if "call" in phone_action1 and ("police" in phone_action1 or "ambulance" in phone_action1 or "emergency" in phone_action1):
		sleep(1.2)
		print "\nYou dial the emergency services and inform them of you accident. Good job!"
		print "You're told that an ambulance has been sent towards you."
		print "You lie to wait for the medics to arrive and assist you get out of the wreck.\n"
		call_of_help(not is_hurt, True, 0)
	elif "call" in phone_action1:
		sleep(1.2)
		print "You dial the number but the target doesn't pick up the phone."
		print "\"What? What time could it be?\""
		print "Your phone reveals that it is 12 : 18 AM."
		sleep(1.5)
		fumble(is_hurt, True)
	else:
		fumble(is_hurt, True)
		
def fumble(is_hurt, has_phone):
	print """
	\rYou keep looking around %s and you realise that
	\rthe light in your car is coming from outside.
	\rThere's a pair of headlights projecting in the direction of your car from ahead.
	\rAs you look at the vehicle ahead you hear something.
	""" % "and fumbling with the phone" if has_phone else ""
	call_of_help(not is_hurt, False, 0)