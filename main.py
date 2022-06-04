import pygame as p
import random

# Some constants
FPS = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)


# Draw 4 figures with period 2 - by pressing "1" in the program
def draw_periodic_figures():
    global cells
    cells = [[0] * field_size for _ in range(field_size)]
    cells[1][1] = 1
    cells[1][2] = 1
    cells[2][1] = 1
    cells[3][4] = 1
    cells[4][3] = 1
    cells[4][4] = 1

    cells[3][8] = 1
    cells[3][9] = 1
    cells[3][10] = 1

    cells[8][1] = 1
    cells[8][3] = 1
    cells[7][3] = 1
    cells[9][2] = 1
    cells[9][4] = 1
    cells[10][2] = 1

    cells[8][7] = 1
    cells[9][7] = 1
    cells[10][8] = 1
    cells[7][9] = 1
    cells[8][10] = 1
    cells[9][10] = 1

    # for a in range(field_size):
    #     for b in range(field_size):
    #         if cells[a][b] == 1:
    #             p.draw.rect(screen, WHITE, (50 * b, 50 * a, 50, 50))
    #         else:
    #             p.draw.rect(screen, BLACK, (50 * b, 50 * a, 50, 50))
    draw_lines()
    p.display.flip()


# Draw a glider - by pressing "2" in the program
def draw_glider():
    global cells
    cells = [[0] * field_size for _ in range(field_size)]

    cells[2][0] = 1
    cells[2][1] = 1
    cells[2][2] = 1
    cells[1][2] = 1
    cells[0][1] = 1

    for a in range(field_size):
        for b in range(field_size):
            if cells[a][b] == 1:
                p.draw.rect(screen, WHITE, (cell_size * b, cell_size * a, cell_size, cell_size))
            else:
                p.draw.rect(screen, BLACK, (cell_size * b, cell_size * a, cell_size, cell_size))
    draw_lines()
    p.display.flip()


# Draw a figure with a period of 8 - by pressing "3" in the program
def draw_eight_periodic_figure():
    global cells
    cells = [[0] * field_size for _ in range(field_size)]

    for a in range(3, 6):
        for b in range(3, 6):
            cells[a][b] = 1
    for a in range(6, 9):
        for b in range(6, 9):
            cells[a][b] = 1

    for a in range(field_size):
        for b in range(field_size):
            if cells[a][b] == 1:
                p.draw.rect(screen, WHITE, (cell_size * b, cell_size * a, cell_size, cell_size))
            else:
                p.draw.rect(screen, BLACK, (cell_size * b, cell_size * a, cell_size, cell_size))
    draw_lines()
    p.display.flip()


# Function to eliminate "edge effects"
def is_tor(x):
    return x % field_size


# Calculating the number of "living" neighbors
# by Moore's neighborhood and Von Neumann's neighborhood
def moore_neighborhood(x, y):
    result = 0
    for t in range(-1, 2):
        for k in range(-1, 2):
            result += cells[is_tor(x+t)][is_tor(y+k)]
    return result - cells[x][y]


def von_neumann_neighborhood(x, y):
    return cells[is_tor(x-1)][is_tor(y)] + cells[is_tor(x+1)][is_tor(y)] + cells[is_tor(x)][is_tor(y-1)] + cells[is_tor(x)][is_tor(y+1)]


# Cell state calculating function for the game "Life",
# wave automaton and fractal automaton
def cell_function_life(x, y):
    neighbours_number = moore_neighborhood(x, y)
    if cells[x][y] == 0 and neighbours_number == 3:
        next_step[x][y] = 1
    else:
        if cells[x][y] == 1 and neighbours_number in {2, 3}:
            next_step[x][y] = 1
        else:
            next_step[x][y] = 0


def cell_function_waves(x, y):
    white = 0
    gray = 0
    black = 0
    for t in range(-1, 2):
        for k in range(-1, 2):
            if cells[is_tor(x + t)][is_tor(y + k)] == 2:
                gray += 1
            else:
                if cells[is_tor(x + t)][is_tor(y + k)] == 0:
                    black += 1
                else:
                    white += 1

    if cells[x][y] == 0 and white >= 3:
        next_step[x][y] = 1
    if cells[x][y] == 2 and black >= 3:
        next_step[x][y] = 0
    if cells[x][y] == 1 and gray >= 3:
        next_step[x][y] = 2


def cell_function_fractals(x, y):
    neighbours_number = moore_neighborhood(x, y)
    if neighbours_number in A:
        next_step[x][y] = 1


# Draw lines on the field
def draw_lines():
    for n in range(field_size):
        p.draw.line(screen, LINES_COLOR, (cell_size * n, 0), (cell_size * n, WINDOW_SIZE))
        p.draw.line(screen, LINES_COLOR, (0, cell_size * n), (WINDOW_SIZE, cell_size * n))


# Calculate the next state of the field
def calculate_next_step(function):
    for a in range(field_size):
        for b in range(field_size):
            function(a, b)


# Drawing the next state for an automaton with 2 cell states
def draw_next_step_two_colors():
    for a in range(field_size):
        for b in range(field_size):
            cells[a][b] = next_step[a][b]
            if cells[a][b] == 1:
                p.draw.rect(screen, WHITE, (cell_size * b, cell_size * a, cell_size, cell_size))
            else:
                if cells[a][b] == 0:
                    p.draw.rect(screen, BLACK, (cell_size * b, cell_size * a, cell_size, cell_size))


# Drawing the next state for an automaton with 3 cell states
def draw_next_step_three_colors():
    for a in range(field_size):
        for b in range(field_size):
            cells[a][b] = next_step[a][b]
            if cells[a][b] == 1:
                p.draw.rect(screen, WHITE, (cell_size * b, cell_size * a, cell_size, cell_size))
            else:
                if cells[a][b] == 0:
                    p.draw.rect(screen, BLACK, (cell_size * b, cell_size * a, cell_size, cell_size))
                else:
                    p.draw.rect(screen, GRAY, (cell_size * b, cell_size * a, cell_size, cell_size))


# Initial random filling of the field (2 or 3 colors)
def random_start_position(colors_number):
    if colors_number == 2:
        for i in range(field_size):
            for j in range(field_size):
                a = random.random()
                if a > 0.5:
                    next_step[i][j] = 0
                else:
                    next_step[i][j] = 1
    else:
        for i in range(field_size):
            for j in range(field_size):
                a = random.random()
                if a < 1/3:
                    next_step[i][j] = 0
                else:
                    if a > 2/3:
                        next_step[i][j] = 1
                    else:
                        next_step[i][j] = 2


# One cell in the center of the field
# (for an automaton with "undying" cells)
def fractals_start_position():
    next_step[field_size // 2][field_size // 2] = 1


# Different cellular automata
def fractal_automaton():
    fractals_start_position()
    draw_next_step_two_colors()
    calculate_next_step(cell_function_fractals)
    draw_lines()
    p.display.flip()
    # Основной цикл игры
    running = 1
    while running:
        for event in p.event.get():  # Закрытие окна при нажатии на крест
            if event.type == p.QUIT:
                running = 0

            if event.type == p.KEYDOWN:  # Считывание нажатой клавиши

                if event.key == p.K_SPACE:  # Следующее поколение при нажатии на "пробел"

                    calculate_next_step(cell_function_fractals)
                    draw_next_step_two_colors()
                    draw_lines()
                    p.display.flip()

        keys = p.key.get_pressed()
        if keys[p.K_SPACE]:
            calculate_next_step(cell_function_fractals)
            draw_next_step_two_colors()
            draw_lines()
            p.display.flip()


def wave_automaton():
    random_start_position(3)
    draw_next_step_three_colors()
    calculate_next_step(cell_function_waves)
    draw_lines()
    p.display.flip()
    # Основной цикл игры
    running = 1
    while running:
        for event in p.event.get():  # Закрытие окна при нажатии на крест
            if event.type == p.QUIT:
                running = 0

            if event.type == p.KEYDOWN:  # Считывание нажатой клавиши

                if event.key == p.K_SPACE:  # Следующее поколение при нажатии на "пробел"

                    calculate_next_step(cell_function_waves)
                    draw_next_step_three_colors()
                    draw_lines()
                    p.display.flip()

        keys = p.key.get_pressed()
        if keys[p.K_SPACE]:
            calculate_next_step(cell_function_waves)
            draw_next_step_three_colors()
            draw_lines()
            p.display.flip()


def life_automaton():
    random_start_position(2)
    draw_next_step_two_colors()
    calculate_next_step(cell_function_life)
    draw_lines()
    p.display.flip()
    # Основной цикл игры
    running = 1
    while running:
        for event in p.event.get():  # Закрытие окна при нажатии на крест
            if event.type == p.QUIT:
                running = 0

            if event.type == p.KEYDOWN:  # Считывание нажатой клавиши

                if event.key == p.K_1:  # Отрисовать периодические фигуры при нажатии на "1"
                    draw_periodic_figures()

                if event.key == p.K_2:  # Отрисовать глайдер при нажатии на "2"
                    draw_glider()

                if event.key == p.K_3:  # Отрисовать 8-периодическую фигуру при нажатии на "3"
                    draw_eight_periodic_figure()

                if event.key == p.K_SPACE:  # Следующее поколение при нажатии на "пробел"

                    calculate_next_step(cell_function_life)
                    draw_next_step_two_colors()
                    draw_lines()
                    p.display.flip()

        keys = p.key.get_pressed()
        if keys[p.K_SPACE]:
            calculate_next_step(cell_function_life)
            draw_next_step_two_colors()
            draw_lines()
            p.display.flip()


# Field size in cells, cell size in pixels
field_size = 70
cell_size = 7

# A set containing the number of necessary neighbors
# for cell nucleation in the fractal automaton
A = {1, 3}

# The color of the lines between the cells
LINES_COLOR = GREEN


# Cell lists
cells = [[0] * field_size for _ in range(field_size)]
next_step = [[0] * field_size for _ in range(field_size)]

# Creating a window with the game
WINDOW_SIZE = cell_size * field_size
p.init()
p.mixer.init()
screen = p.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
p.display.set_caption("Automaton")

# Starting up the machine
life_automaton()
# wave_automaton()
# fractal_automaton()

p.quit()
