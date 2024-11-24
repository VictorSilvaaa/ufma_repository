# tamanho de tela
WIDTH, HEIGHT = 800, 600

# cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# recursos
RESOURCE_TYPES = {
    "energetic_crystal": {"color": GREEN, "size": 5, "utility": 10, "agents_required": 1, 'img': 'energetic_crystal.png'},
    "rare_metal_block": {"color": BLUE, "size": 10, "utility": 20, "agents_required": 1, 'img': 'rare_metal_block.png'},
    "ancient_structure": {"color": RED, "size": 15, "utility": 50, "agents_required": 2,'img': 'ancient_structure.png'},
}

# Definindo o tamanho da célula da grade (o tamanho de cada quadrado)
GRID_SIZE = 50

# Definindo o número de células na horizontal e vertical
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

ROWS = HEIGHT // GRID_SIZE
COLS = WIDTH // GRID_SIZE

PATH_IMGS = "./imgs/"