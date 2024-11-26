import random
from configs import *
from resource import Resource
from obstacle import Obstacle
import heapq

# Função para gerar um recurso aleatório
def generate_random_resource(matrix):
    resource_type = random.choice(list(RESOURCE_TYPES.keys()))

    flag = True
    while flag:
        x = random.randint(0, (WIDTH//GRID_SIZE - 1))
        y = random.randint(0, (HEIGHT//GRID_SIZE - 1))
        if len(matrix[y][x]) == 0: 
            flag = False

    resource = Resource(resource_type, x, y)
    return resource

def generate_random_obstacle(matrix):
    obstacle_type = random.choice(list(OBSTACLE_TYPES.keys()))

    flag = True
    while flag:
        x = random.randint(0, (WIDTH // GRID_SIZE - 1))
        y = random.randint(0, (HEIGHT // GRID_SIZE - 1))
        if len(matrix[y][x]) == 0:  # A célula deve estar vazia
            flag = False

    obstacle = Obstacle(obstacle_type, x, y)
    return obstacle

def generate_obstacle_lines(matrix, num_lines):
    for _ in range(num_lines):
        obstacle_type = random.choice(list(OBSTACLE_TYPES.keys()))
        y = random.randint(0, ROWS - 1)  # Escolhe uma linha aleatória
        for x in range(COLS):  # Preenche toda a linha com o mesmo tipo de obstáculo
            if len(matrix[y][x]) == 0:  # Certifica-se de que a célula está vazia
                obstacle = Obstacle(obstacle_type, x, y)
                matrix[y][x].append(obstacle)


def get_null_positon(matrix):
    flag = True
    while flag:
        x = random.randint(0, (WIDTH//GRID_SIZE - 1))
        y = random.randint(0, (HEIGHT//GRID_SIZE - 1))
        if len(matrix[y][x]) == 0 and x!= INITIAL_POS['x']  and y!= INITIAL_POS['y']: 
            flag = False

    return {"x": x, "y": y}

# Função para verificar colisão entre agente e um recurso
def check_collision(agent_x, agent_y, resource_x, resource_y, agent_size):
    distance = ((agent_x - resource_x) ** 2 + (agent_y - resource_y) ** 2) ** 0.5
    return distance < (agent_size + 15)  # Ajuste para colisão

# Função para converter as coordenadas do agente para a posição central da grade
def convert_to_grid_pos(x, y):
    grid_x = x * GRID_SIZE + GRID_SIZE // 2
    grid_y = y * GRID_SIZE + GRID_SIZE // 2
    return grid_x, grid_y

# Heurística de Manhattan
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(start, goal, matrix, obstacles, resources):
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            # Reconstrói o caminho a partir de `came_from`
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # Movimentos possíveis (cima, baixo, esquerda, direita) e diagonais (apenas variações de -1, 0 ou 1)
        neighbors = [
            (current[0] + dx, current[1] + dy)
            for dx in [-1, 0, 1]  # Para X
            for dy in [-1, 0, 1]  # Para Y
            if (dx != 0 or dy != 0)  # Ignora o movimento (0, 0)
        ]

        for neighbor in neighbors:
            if (
                0 <= neighbor[0] < len(matrix[0]) and  # Limites do grid (x)
                0 <= neighbor[1] < len(matrix) and  # Limites do grid (y)
                neighbor not in obstacles  # Verifica se não é um obstáculo
            ):
                # Verifica se o vizinho é um recurso que precisa de dois agentes
                is_resource_with_two_agents = any(
                    r.x == neighbor[0] and r.y == neighbor[1] and r.agents_required == 2
                    for r in resources
                )

                # Se o recurso precisa de dois agentes, e não é o objetivo do agente, ignora o vizinho
                if is_resource_with_two_agents and neighbor != goal:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Atualiza a melhor rota conhecida para este vizinho
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

