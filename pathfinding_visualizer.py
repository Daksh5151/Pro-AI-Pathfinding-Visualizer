# advanced_pathfinding_visualizer.py
# An advanced tool to visualize and compare pathfinding algorithms with a modern UI.

# --- 1. IMPORT LIBRARIES ---
import pygame
import math
from queue import PriorityQueue
import random
from collections import deque

# --- 2. SETUP PYGAME WINDOW AND UI ---
GRID_WIDTH = 800
PANEL_WIDTH = 250
WIDTH = GRID_WIDTH + PANEL_WIDTH
WIN = pygame.display.set_mode((WIDTH, GRID_WIDTH))
pygame.display.set_caption("Pro AI Pathfinding Visualizer")
pygame.font.init()

# --- 3. DEFINE COLORS ---
RED = (255, 87, 51)         # Closed nodes
GREEN = (46, 204, 113)      # Open nodes
BLUE = (52, 152, 219)       # Path
YELLOW = (241, 196, 15)     # Weighted nodes ("mud")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)           # Barriers
PURPLE = (142, 68, 173)     # Final Path
ORANGE = (230, 126, 34)     # Start node
GREY = (224, 224, 224)      # Grid lines
TURQUOISE = (26, 188, 156)  # End node
PANEL_BG = (44, 62, 80)     # UI Panel Background
TEXT_COLOR = (236, 240, 241)

# --- 4. CREATE THE NODE/SPOT CLASS ---
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self): return self.row, self.col
    def is_closed(self): return self.color == RED
    def is_open(self): return self.color == GREEN
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_end(self): return self.color == TURQUOISE
    def is_weight(self): return self.color == YELLOW
    def reset(self): self.color = WHITE
    def make_start(self): self.color = ORANGE
    def make_closed(self): self.color = RED
    def make_open(self): self.color = GREEN
    def make_barrier(self): self.color = BLACK
    def make_end(self): self.color = TURQUOISE
    def make_path(self): self.color = PURPLE
    def make_weight(self): self.color = YELLOW
    def draw(self, win): pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other): return False

# --- 5. UI BUTTON CLASS ---
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, win):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(win, current_color, self.rect, border_radius=8)
        
        font = pygame.font.SysFont('helveticaneue', 20)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        win.blit(text_surf, (self.rect.centerx - text_surf.get_width() // 2, self.rect.centery - text_surf.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# --- 6. ALGORITHM IMPLEMENTATIONS (Identical to before) ---
def h(p1, p2): # Heuristic for A*
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    path_length = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path_length += 1
        draw()
    return path_length

def a_star_dijkstra(draw, grid, start, end, use_astar=True):
    count = 0; open_set = PriorityQueue(); open_set.put((0, count, start)); came_from = {}; g_score = {spot: float("inf") for row in grid for spot in row}; g_score[start] = 0; f_score = {spot: float("inf") for row in grid for spot in row}; f_score[start] = h(start.get_pos(), end.get_pos()) if use_astar else 0; open_set_hash = {start}; nodes_visited = 0
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
        current = open_set.get()[2]; open_set_hash.remove(current); nodes_visited += 1
        if current == end:
            path_length = reconstruct_path(came_from, end, draw); end.make_end(); start.make_start(); return True, path_length, nodes_visited
        for neighbor in current.neighbors:
            cost = 10 if neighbor.is_weight() else 1 # Increased weight cost
            temp_g_score = g_score[current] + cost
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current; g_score[neighbor] = temp_g_score; f_score[neighbor] = temp_g_score + (h(neighbor.get_pos(), end.get_pos()) if use_astar else 0)
                if neighbor not in open_set_hash:
                    count += 1; open_set.put((f_score[neighbor], count, neighbor)); open_set_hash.add(neighbor); neighbor.make_open()
        if current != start: current.make_closed()
    return False, 0, nodes_visited

def breadth_first_search(draw, grid, start, end):
    queue = deque([start]); came_from = {}; visited = {start}; nodes_visited = 1
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
        current = queue.popleft(); nodes_visited += 1
        if current == end:
            path_length = reconstruct_path(came_from, end, draw); end.make_end(); start.make_start(); return True, path_length, nodes_visited
        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current; visited.add(neighbor); queue.append(neighbor); neighbor.make_open()
        if current != start: current.make_closed()
    return False, 0, nodes_visited

# --- 7. MAZE GENERATION ---
def generate_maze(grid):
    for row in grid:
        for spot in row:
            if random.random() < 0.3: spot.make_barrier()

# --- 8. DRAWING AND UI FUNCTIONS ---
def make_grid(rows, width):
    grid = []; gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows); grid[i].append(spot)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows): pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows): pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_ui(win, buttons, ui_info):
    pygame.draw.rect(win, PANEL_BG, (GRID_WIDTH, 0, PANEL_WIDTH, GRID_WIDTH))
    
    font_title = pygame.font.SysFont('helveticaneue', 28, bold=True)
    font_sub = pygame.font.SysFont('helveticaneue', 20)
    font_info = pygame.font.SysFont('helveticaneue', 16)
    
    title = font_title.render("CONTROLS", 1, WHITE)
    win.blit(title, (GRID_WIDTH + PANEL_WIDTH // 2 - title.get_width() // 2, 20))
    
    for button in buttons: button.draw(win)

    if ui_info['algo_running']:
        status_text = font_sub.render(f"Running: {ui_info['algo_name']}", 1, YELLOW)
        win.blit(status_text, (GRID_WIDTH + PANEL_WIDTH // 2 - status_text.get_width() // 2, 450))

    if ui_info['solved']:
        path_text = font_sub.render(f"Path Length: {ui_info['path']}", 1, GREEN)
        visited_text = font_sub.render(f"Nodes Visited: {ui_info['visited']}", 1, RED)
        win.blit(path_text, (GRID_WIDTH + PANEL_WIDTH // 2 - path_text.get_width() // 2, 500))
        win.blit(visited_text, (GRID_WIDTH + PANEL_WIDTH // 2 - visited_text.get_width() // 2, 530))
    
    # Instructions
    instructions = [
        "LMB: Place Start/End/Walls", "MMB: Place Weights ('Mud')",
        "RMB: Erase Node", "C Key: Clear Grid"
    ]
    for i, text in enumerate(instructions):
        inst_text = font_info.render(text, 1, GREY)
        win.blit(inst_text, (GRID_WIDTH + 15, 600 + i * 25))


def draw(win, grid, rows, width, buttons, ui_info):
    win.fill(WHITE)
    for row in grid:
        for spot in row: spot.draw(win)
    draw_grid_lines(win, rows, width)
    draw_ui(win, buttons, ui_info)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows; y, x = pos
    if y > width: return None # Clicked on panel
    return y // gap, x // gap

# --- 9. MAIN FUNCTION ---
def main(win, width):
    ROWS = 50; grid = make_grid(ROWS, GRID_WIDTH); start = None; end = None; run = True
    
    ui_info = { 'algo_running': False, 'algo_name': '', 'solved': False, 'path': 0, 'visited': 0 }

    buttons = [
        Button(GRID_WIDTH + 25, 100, 200, 40, "Run A* Search (A)", (52, 152, 219), (41, 128, 185)),
        Button(GRID_WIDTH + 25, 150, 200, 40, "Run Dijkstra's (D)", (52, 152, 219), (41, 128, 185)),
        Button(GRID_WIDTH + 25, 200, 200, 40, "Run BFS (B)", (52, 152, 219), (41, 128, 185)),
        Button(GRID_WIDTH + 25, 300, 200, 40, "Generate Maze (M)", (231, 76, 60), (192, 57, 43)),
        Button(GRID_WIDTH + 25, 350, 200, 40, "Clear Grid (C)", (127, 140, 141), (149, 165, 166))
    ]

    while run:
        draw(win, grid, ROWS, GRID_WIDTH, buttons, ui_info)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False

            # Button Clicks
            for button in buttons:
                if button.handle_event(event):
                    if "A*" in button.text: pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
                    if "Dijkstra" in button.text: pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
                    if "BFS" in button.text: pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b))
                    if "Maze" in button.text: pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m))
                    if "Clear" in button.text: pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c))
            
            # Grid Clicks
            pos = pygame.mouse.get_pos()
            clicked_grid_pos = get_clicked_pos(pos, ROWS, GRID_WIDTH)
            if clicked_grid_pos:
                row, col = clicked_grid_pos
                spot = grid[row][col]
                if pygame.mouse.get_pressed()[0]: # LMB
                    if not start and spot != end: start = spot; start.make_start()
                    elif not end and spot != start: end = spot; end.make_end()
                    elif spot != end and spot != start: spot.make_barrier()
                elif pygame.mouse.get_pressed()[1]: # MMB
                    if spot != start and spot != end: spot.make_weight()
                elif pygame.mouse.get_pressed()[2]: # RMB
                    spot.reset();
                    if spot == start: start = None
                    if spot == end: end = None
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_b) and start and end:
                    for r in grid:
                        for s in r: s.update_neighbors(grid)
                    
                    ui_info['algo_running'] = True; ui_info['solved'] = False
                    if event.key == pygame.K_a:
                        ui_info['algo_name'] = "A* Search"; solved, path, visited = a_star_dijkstra(lambda: draw(win, grid, ROWS, GRID_WIDTH, buttons, ui_info), grid, start, end, use_astar=True)
                    elif event.key == pygame.K_d:
                        ui_info['algo_name'] = "Dijkstra's"; solved, path, visited = a_star_dijkstra(lambda: draw(win, grid, ROWS, GRID_WIDTH, buttons, ui_info), grid, start, end, use_astar=False)
                    elif event.key == pygame.K_b:
                        ui_info['algo_name'] = "BFS"; solved, path, visited = breadth_first_search(lambda: draw(win, grid, ROWS, GRID_WIDTH, buttons, ui_info), grid, start, end)

                    ui_info['algo_running'] = False
                    if solved: ui_info['solved'] = True; ui_info['path'] = path; ui_info['visited'] = visited

                if event.key == pygame.K_m:
                    start = None; end = None; grid = make_grid(ROWS, GRID_WIDTH); generate_maze(grid); ui_info['solved'] = False
                if event.key == pygame.K_c:
                    start = None; end = None; grid = make_grid(ROWS, GRID_WIDTH); ui_info['solved'] = False

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)

