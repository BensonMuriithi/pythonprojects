from time import sleep

def ambulance_arrive(has_helped):
	if has_helped:
		epillipsis()
		sleep(2)
		print """
		\rTwo ambulances arrive with blaring sirens.
		\rThey halt ahead of you and several medics rush out of them towards you, the lady and her son.
		\rThey tend to each of you separately and one attending to you asks you something.
		\rAs she does you see a police car racing to the scene.
		\rThe voices all around you seem to fade""",
		sleep(1.5)
	else:
		print "You wait in your car for an ambulance to come."
		epillipsis()
		sleep(2)
		print """
		\rTwo ambulances arrive with blaring sirens.
		\rThe voice from the car crashed ahead of you calls out for help.
		\rSome medics rush to the car and others rushes to yours.
		\rYou also call for help as the medics approaches.
		\rThe medics begin asking you some questions as they asses how to get you ou of the car.
		\rYou see the lights of a police car racing to the scene.""",
		
	finish()
		

def die(has_helped):
	if not has_helped:
		print "You stay in the car still befuddled by your sorroundings."
		epillipsis()
		print """
		\rYou see a set of headlights coming up the opposite side of the hill
		\r"I hope this driver stops to help me."""
		sleep(1)
		print """\rThe vehicle gets closer to the summit and you hold your guts hoping the driver stops
		\rAfter reaching the summit the vehicle looks towards descent
		\rSomething, probably your headlights disorients the approaching driver as the vehicle 
		\rstarts to swerve across the road.
				"Oh God!!\"""",
	else:
		wake_peter()
		print """
		\rThe lady directs you to approaching headlights ascending the hill
		\rfrom the direction she came."""
		sleep(1)
		print """\r"Oh, thankyou!!" You blurt in exhileration.
		\rThe vehicle gets closer to the summit and you hold your guts hoping the driver stops
		\rAfter reaching the summit the vehicle looks towards descent"""
		sleep(1)
		print"""\rSomething, probably your headlights, disorients the approaching driver as the vehicle 
		\rstarts to swerve across the road.
				"Oh God!!\"""",
				
	finish()
		
def finish():
	sleep(0.72)
	epillipsis()
	sleep(9)
	
def epillipsis():
	for i in range(0, 6):
		sleep(0.2)
		print ".",
		
def wake_peter():
	print """
	\rYou all stay on the ground all seemingly hurt
	\rThe lady tries to wake her son by calling his name.
	"""
	sleep(0.6)
	print "PETER! PETER!"
	sleep(0.4)
	print "Peter wake up!"
	sleep(0.35)
	print "PETER PLEASE!"
	sleep(1.2)
	
