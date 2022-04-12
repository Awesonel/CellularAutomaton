import pygame as p
import random

# Некоторые константы
field_size = 12
WINDOW_SIZE = 50 * field_size

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Списки клеток
cells = [[0] * field_size for _ in range(field_size)]
next_step = [[0] * field_size for _ in range(field_size)]


# Нарисовать 4 фигуры с периодом 2 - при нажатии на "1" в программе
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

    for a in range(field_size):
        for b in range(field_size):
            if cells[a][b] == 1:
                p.draw.rect(screen, WHITE, (50 * b, 50 * a, 50, 50))
            else:
                p.draw.rect(screen, BLACK, (50 * b, 50 * a, 50, 50))
    draw_lines()
    p.display.flip()


# Нарисовать планер (глайдер) - при нажатии на "2" в программе
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
                p.draw.rect(screen, WHITE, (50 * b, 50 * a, 50, 50))
            else:
                p.draw.rect(screen, BLACK, (50 * b, 50 * a, 50, 50))
    draw_lines()
    p.display.flip()


# Нарисовать фигуру с периодом 8 - при нажатии на "3" в программе
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
                p.draw.rect(screen, WHITE, (50 * b, 50 * a, 50, 50))
            else:
                p.draw.rect(screen, BLACK, (50 * b, 50 * a, 50, 50))
    draw_lines()
    p.display.flip()


# Функция устранения "краевых эффектов"
def is_tor(x):
    return x % field_size


# Подсчёт количества "живых" соседей
def count_neighbours(x, y):
    result = 0
    for t in range(-1, 2):
        for k in range(-1, 2):
            result += cells[is_tor(x+t)][is_tor(y+k)]
    return result - cells[x][y]


# Функция подсчёта состояния клетки
def cell_function(x, y):
    neighbours_number = count_neighbours(x, y)
    if cells[x][y] == 0 and neighbours_number == 3:
        next_step[x][y] = 1
    else:
        if cells[x][y] == 1 and neighbours_number in {2, 3}:
            next_step[x][y] = 1
        else:
            next_step[x][y] = 0


# Отрисовка линий на поле
def draw_lines():
    for n in range(field_size):
        p.draw.line(screen, RED, (50 * n, 0), (50 * n, WINDOW_SIZE))
        p.draw.line(screen, RED, (0, 50 * n), (WINDOW_SIZE, 50 * n))


# Подсчёт следующего состояния поля
def calculate_next_step():
    for a in range(field_size):
        for b in range(field_size):
            cell_function(a, b)


# Отрисовка следующего состояния
def draw_next_step():
    for a in range(field_size):
        for b in range(field_size):
            cells[a][b] = next_step[a][b]
            if cells[a][b] == 1:
                p.draw.rect(screen, WHITE, (50 * b, 50 * a, 50, 50))
            else:
                p.draw.rect(screen, BLACK, (50 * b, 50 * a, 50, 50))


# Создание окна с игрой
p.init()
p.mixer.init()
screen = p.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
p.display.set_caption("My Game")
screen.fill(BLACK)

# Начальное случайное заполнение поля
for i in range(field_size):
    for j in range(field_size):
        cells[i][j] = random.randint(0, 1)
calculate_next_step()
draw_next_step()
draw_lines()
p.display.flip()

# Основной цикл игры
running = 1
while running:

    for event in p.event.get():         # Закрытие окна при нажатии на крест
        if event.type == p.QUIT:
            running = 0

        if event.type == p.KEYDOWN:     # Считывание нажатой клавиши

            if event.key == p.K_1:      # Отрисовать периодические фигуры при нажатии на "1"
                draw_periodic_figures()

            if event.key == p.K_2:      # Отрисовать глайдер при нажатии на "2"
                draw_glider()

            if event.key == p.K_3:      # Отрисовать 8-периодическую фигуру при нажатии на "3"
                draw_eight_periodic_figure()

            if event.key == p.K_SPACE:  # Следующее поколение при нажатии на "пробел"

                calculate_next_step()
                draw_next_step()
                draw_lines()
                p.display.flip()

p.quit()
