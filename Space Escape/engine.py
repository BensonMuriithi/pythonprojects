from death import Death
from central_corridor import CentralCorridor
from armory import Armory
from bridge import Bridge
from escape_pod import EscapePod
from control_room import ControlRoom

class Engine(object):
	"""Game engine of the space escape game. Invocations on scenes to run are made by other scenes
	ie After the starting scene, a line in that scene invokes the next scene via this engine"""
	def __init__(self):
		self.has_plasmagun = False
		self.has_teslagun = False
		self.has_flamethrower = False
		self.has_timebomb = False
		self.bomb_set = False
		
		self.current_scene = None
		
	def has_gun(self):
		return self.has_flamethrower or self.has_plasmagun or self.has_teslagun
		
	def play(self):
		self.current_scene = ControlRoom()
		self.current_scene.enter(self)
		
	def central_corridor(self):
		self.current_scene = CentralCorridor()
		self.current_scene.enter(self)
		
	def armory(self):
		self.current_scene = Armory()
		self.current_scene.enter(self)
		
	def bridge(self):
		self.current_scene = Bridge()
		self.current_scene.enter(self)
		
	def escape_pod(self):
		self.current_scene = EscapePod()
		self.current_scene.enter(self)
		
	def death(self):
		self.current_scene = Death()
		self.current_scene.enter()