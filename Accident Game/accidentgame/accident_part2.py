from time import sleep
from accident_part3 import die
from accident_part3 import ambulance_arrive

def call_of_help(can_help, has_called_amb, num_ignored):
	ignored = num_ignored
	
	sounds_of_help(ignored == 0)
	
	help_action = raw_input("> ").lower()
	if "go" in help_action or "out" in help_action or "help" in help_action:
		try_to_help(can_help, has_called_amb)
	elif "listen" in help_action or "wait" in help_action or "hear" in help_action:
		ignored += 1
		call_of_help(can_help, has_called_amb, ignored)
	else:
		ignored += 1
		call_of_help(can_help, has_called_amb, ignored) if ignored <= 1 else wait_in_car(has_called_amb)
		
def sounds_of_help(first_call):
	sleep(4.2)
	if first_call:
		print "\n\"HELP! HELP! HELP!\""
		print "The sounds are coming from the car halted ahead of yours"
		print "and the voice sounds as if it's of a woman."
		print "\"HELP! HEELP! HEEELP!\""
		print "The voice sounds as if it's of a woman and is getting more intense."
		print "The person sounds to be in dire distress."
	else:
		print "\n\"HELP! HELP! HELP!\""
		print "\"HELP! HEELP! HEEELP!\""
		
	print "What do you do?"

def wait_in_car(has_called_amb):
	ambulance_arrive(False) if has_called_amb else die(False)
	
def try_to_help(can_help, has_called_amb):
	if not can_help:
		print """
		\rYou try to lift the dashboard off of your legs
		\rYou scream in pain as a sharp pain comes from your shoulder.
		\rYou fear that if you push yourself you will injure yourself badly.
		"""
		if has_called_amb:
			sleep(1)
			print "It's better you stay put to avoid further injury to yourself."
			print "You can only hope that the lady is not fatally injured."
			tic_toc_wait()
			ambulance_arrive(False)
		else:
			call_again(False)
	else: 
		get_to_car()
		mom_talk(has_called_amb, False)

def call_again(has_helped):
	if not has_helped:
		print "You should call an ambulance to help you and the lady in the other car."
		call = raw_input("Do you? >> ").lower()
		if "no" in call or "don't" in call:
			die(False)
		elif "yes" in call or "yeah" in call or "okay" in ambulance:
			sleep(1.2)
			print "The ambulance is on it's way."
			ambulance_arrive(False)
	else:
		print "\t\"Call an ambulance!\""
		to_call = raw_input("Do you? > ").lower()
		
		if "no" in to_call or "don't" in to_call or "not" in to_call:
			die(True)
		elif "yes" in to_call or "call" in to_call or "yea" in to_call:
			sleep(1.2)
			print "\"The ambulance is on it's way.\""
			ambulance_arrive(True)
			
			
def get_to_car():
	sleep(1)
	print """
	\rYou try as hard as you can to lift the dashboard off your legs
	\rYour legs slowly get free and you struggle out of the car carefully to avoid hurting yourself
	\rSteadily you manage to pull yourself from the car and get to your feet
	\rYou limp towards the other wreck.
	"""
	sleep(3)
	print """
	\rYou get to an overturned SUV
	\rYou crouch to look into the car and see if there's a person inside
	\rThere's a lady suspended upside down by her seatbelt
	\rShe looks anxiously at you.\n
	\r"OH THANK YOU! PLEASE CHECK IF MY SON IS OKAY!"
	\r"PLEASE CHECK IF HE'S OKAY! HE'S IN THE BACK PLEASE CHECK IF HE'S OKAY!"
	\r"OH, GOD!!"
	"""
	
def plead():
	print "PLEASE CHECK IF MY BOY'S OKAY!!"
	print "PLEASE! HELP ME!!"
	

def mom_talk(has_called_amb, was_ignored):
	has_ignored = was_ignored
	plead() if has_ignored else get_to_car()
	save_boy = raw_input("\nPlease do something! >>> " if has_ignored else "Do something! >>> ").lower()
	if "back" in save_boy or "save" in save_boy or "help" in save_boy or "rush" in save_boy or "check" in save_boy or "look" in save_boy:
		print """
		\rThere's a young boy seemingly below 6 years old suspended in a seat-belt
		\rAs you fear his demise you notice that he has a thick jacket that could have protected his body
		\rYou tell the boy's mother that the boy could be alright.
		\rHolding on to your own hope, the mother is struggling to not break down in sorrow.
		"""
		helping_boy()
		helping_mom(has_called_amb)
	else:
		mom_talk(has_called_amb, True)
	
def check_pulse():
	print "You carefully lay him on the ground a step away from the vehicle."
	print "You check the boy's pulse"
	sleep(3)
	print "\"HE'S OKAY!\" You yell to the boy's mother."
	sleep(2)
	print "\"He's okay!\" You say in a calmer tone."

def helping_boy():
	print "What do you do??"
	action1 = raw_input(">> ").lower()
	if "get" in action1 or "help"in action1 or "belt" in action1 or "hurt" in action1 or "out" in action1 or "unsecure" in action1 or "free" in action1:
		print "After carefully unplugging the boy's seatbelt and get him out of the car."
		check_pulse()
	elif "check" in action1 or "pulse" in action1 or "alive" in action1 or "wake" in action1:
		print "You tap the boy slighly on gis cheek. He is not coming around."
		check_pulse()
	else:
		print "\"PLEASE HELP MY SON! PLEASE CHECK IF HE IS ALIVE!!"
		print "\"PLEEASE!!"
		helping_boy()
		
def helping_mom(has_called_amb):
	print """
	\rYou go to help the lady get out of the car.
	\rShe seems to have been cut and injured on her very arm badly.
	\rYou take off her seatbelt help her get out of the car.
	\rShe gets to her feet and trudges towards her son.
	"""
	print "She gets to the ground to touch him and she sighs when she feels him breathing"
	if has_called_amb:
		sleep(0.99)
		print "\n\"I've already called an ambulance.\""
		print "\"It should be here any minute. He's going to be alright."
		sleep(1.2)
		ambulance_arrive(True)
	else:
		call_again(True)
		
def tic_toc_wait():
	words = ["Tic ", "Toc "]
	for i in range(0, 2):
		for w in words:
			sleep(0.7)
			print w,

