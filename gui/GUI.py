import pygame
import sys
from time import sleep
from app.Movement import Movement
from app.Layout import Grid


class Colors:
	WHITE = (255, 255, 255)
	GRAY = (200, 200, 200)
	BLUE = (0, 0, 255)
	RED = (255, 0, 0)
	BLACK = (0, 0, 0)
	GREEN = (0, 255, 0)
	YELLOW = (255, 255, 0)  # to do: increasing gradient


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600  # Screen dimensions
CELL_SIZE = WIDTH // 10  # Size of each grid cell
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# font = pygame.font.Font(None, 18)  # Default font, size 18

# Grid Setup
grid = Grid(ROWS)
move = Movement(grid)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stardew Navigation")

# Track highlighted cells
highlighted_cells = []
dest_set = False
dest_cell = None
src_cell = [0, 0]
path_gen = None

# Game loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = event.pos
			dest_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)
			path_gen = move.shortest_path((src_cell[1], src_cell[0]), dest_cell, mode=2)
			highlighted_cells = []
			dest_set = True

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN and src_cell[0] < ROWS - 1:
				src_cell[0] += 1
				dest_set = False
			elif event.key == pygame.K_UP and src_cell[0] > 0:
				src_cell[0] -= 1
				dest_set = False
			elif event.key == pygame.K_LEFT and src_cell[1] > 0:
				src_cell[1] -= 1
				dest_set = False
			elif event.key == pygame.K_RIGHT and src_cell[1] < COLS - 1:
				src_cell[1] += 1
				dest_set = False

	if dest_cell and not dest_set:
		path_gen = move.shortest_path((src_cell[1], src_cell[0]), dest_cell)
		highlighted_cells = []

	if path_gen:
		try:
			highlighted_cell = next(path_gen)
			highlighted_cells.append(highlighted_cell)
		except StopIteration:
			path_gen = None

	# Draw grid
	screen.fill(Colors.WHITE)
	for row in range(ROWS):
		for col in range(COLS):
			rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			if dest_cell and (col, row) == dest_cell:
				color = Colors.RED
			elif grid.get((col, row)) in highlighted_cells:
				color = Colors.YELLOW
			else:
				color = Colors.GRAY

			pygame.draw.rect(screen, color, rect)
			pygame.draw.rect(screen, Colors.BLUE, rect, 1)  # Grid lines

			# text = font.render(f"({col}, {row})", True, Colors.BLACK)
			# text_rect = text.get_rect(center=rect.center)
			# screen.blit(text, text_rect)

	src_rect = pygame.Rect(src_cell[1] * CELL_SIZE, src_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(screen, Colors.GREEN, src_rect)

	# Update display
	pygame.display.flip()

	sleep(0.1)

# Quit Pygame
pygame.quit()
sys.exit()
