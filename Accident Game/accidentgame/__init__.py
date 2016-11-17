"""initialising script for accident_game, which is more of a narration"""

from .accident_part1 import come_around

def start():
	try:
		come_around()
	except KeyboardInterrupt:
		print()

if __name__ == "__main__":
	start()

