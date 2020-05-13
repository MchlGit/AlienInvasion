import pygame 
from pygame.sprite import Sprite 

class Alien(Sprite): 

	def __init__(self, ai_game): 
		'''Initiate alien and its starting position'''
		super().__init__()
		self.screen = ai_game.screen

		#load alien image and set its rect attribute
		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()

		# Start each new alien new top left of screen.. but how??
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Store alien's exact horizontal position
		self.x = float(self.rect.x)