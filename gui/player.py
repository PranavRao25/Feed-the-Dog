import pygame.sprite


class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, image, speed, cell_size):
		super().__init__()
		self.cell_size = cell_size
		self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.cell_size, self.cell_size))
		self.rect = self.image.get_rect()
		self.rect.center = (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2)
		self.grid_pos = (x, y)
		self.speed = speed
	
	def move_to(self, x, y):
		"""Update player position on the grid."""
		self.grid_pos = (x, y)
		self.rect.center = (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2)