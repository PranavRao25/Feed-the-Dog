import pygame
import sys
import asyncio
from time import sleep
from app.Movement import Movement
from app.Layout import Grid
from gui.player import Player


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600  # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CELL_SIZE = WIDTH // 10  # Size of each grid cell
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
clock = pygame.time.Clock()


class Colors:
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)  # to do: increasing gradient

  
class GridTile(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)


class DestTile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        self.grid_pos = (x, y)
  
  
async def main():
    # Grid Setup
    grid = Grid(ROWS)
    # font = pygame.font.Font(None, 18)  # Default font, size 18
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    
    move = Movement(grid)
    
    # Initialize screen
    
    pygame.display.set_caption("Stardew Navigation")
    
    # Track highlighted cells
    highlighted_cells = []
    highlighted_cell = None
    complete_path = []
    dest_set = False
    dest_cell = None
    src_cell = [0, 0]
    path_gen = None
    player_pos = src_cell.copy()
    next_hop = None
    player = Player(player_pos[0], player_pos[1], "gui/files/dog.png", 2, CELL_SIZE)
    all_sprites.add(player)
    dest_tile = None
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                src_cell = player_pos[::-1]
                if dest_tile and all_sprites:
                    all_sprites.remove(dest_tile)
                
                mouse_x, mouse_y = event.pos
                dest_cell = [mouse_x // CELL_SIZE, mouse_y // CELL_SIZE]
                dest_tile = DestTile(dest_cell[0], dest_cell[1], "gui/files/bone.jpeg")
                all_sprites.add(dest_tile)
                
                dest_set = True
                path_gen = move.shortest_path((src_cell[1], src_cell[0]), tuple(dest_cell))
                highlighted_cells = []
                complete_path = []
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and src_cell[0] < ROWS - 1:
                    src_cell[0] += 1
                elif event.key == pygame.K_UP and src_cell[0] > 0:
                    src_cell[0] -= 1
                elif event.key == pygame.K_LEFT and src_cell[1] > 0:
                    src_cell[1] -= 1
                elif event.key == pygame.K_RIGHT and src_cell[1] < COLS - 1:
                    src_cell[1] += 1
                elif event.key == pygame.K_q:
                    running = False
                else:
                    raise ValueError("Invalid key pressed")
                dest_set = False
        
        if dest_cell and not dest_set:
            path_gen = move.shortest_path((src_cell[1], src_cell[0]), tuple(dest_cell))
            highlighted_cells = []
        
        if path_gen:
            try:
                highlighted_cell = next(path_gen)
                print(highlighted_cell)
                player_pos = [highlighted_cell.x, highlighted_cell.y]
                player.move_to(*player_pos)
                highlighted_cells.append(highlighted_cell)
                complete_path.append(highlighted_cell)
            except StopIteration:
                path_gen = None
                src_cell = [dest_cell[1], dest_cell[0]]
                complete_path = []
                all_sprites.remove(dest_tile)
        
        # Draw grid
        screen.fill(Colors.WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if dest_cell and (col, row) == dest_cell:
                    color = Colors.RED
                elif highlighted_cell and grid.get((col, row)) == highlighted_cell:
                    color = Colors.YELLOW
                elif grid.get((col, row)) in complete_path:
                    color = Colors.ORANGE
                else:
                    color = Colors.GRAY
                
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, Colors.BLUE, rect, 1)  # Grid lines
            
            # text = font.render(f"({col}, {row})", True, Colors.BLACK)
            # text_rect = text.get_rect(center=rect.center)
            # screen.blit(text, text_rect)
        
        src_rect = pygame.Rect(src_cell[1] * CELL_SIZE, src_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, Colors.GREEN, src_rect)
        
        all_sprites.draw(screen)
        
        # Update display
        pygame.display.flip()
        
        sleep(0.1 * player.speed)
    
    # Quit Pygame
    pygame.quit()
    sys.exit()

asyncio.run(main())
