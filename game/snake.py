import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Global constants
WIDTH = 500
ROWS = 20
CELL_SIZE = WIDTH // ROWS

BG_COLOR = (203, 228, 50)
SNAKE_COLOR = (46, 52, 9)
FOOD_COLOR = (253, 77, 12)


class Cube:
    rows = ROWS
    w = WIDTH

    def __init__(self, start, dx=1, dy=0, color=SNAKE_COLOR, head=False):
        self.pos = start
        self.head = head
        self.dx = dx
        self.dy = dy
        self.color = color

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

    def draw(self, surface):
        i, j = self.pos
        pygame.draw.rect(surface, self.color, (i * CELL_SIZE + 1, j * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        if self.head:
            center = CELL_SIZE // 2
            radius = 3
            circle_middle = (i * CELL_SIZE + center - radius, j * CELL_SIZE + 8)
            circle_middle_2 = (i * CELL_SIZE + CELL_SIZE - radius * 2, j * CELL_SIZE + 8)
            pygame.draw.circle(surface, (255, 255, 255), circle_middle, radius)
            pygame.draw.circle(surface, (255, 255, 255), circle_middle_2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos, head=True)
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dx = -1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]
                elif keys[pygame.K_RIGHT]:
                    self.dx = 1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]
                elif keys[pygame.K_UP]:
                    self.dx = 0
                    self.dy = -1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]
                elif keys[pygame.K_DOWN]:
                    self.dx = 0
                    self.dy = 1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

        # Move the body
        for i, cell in enumerate(self.body):
            p = cell.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                cell.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if cell.dx == -1 and cell.pos[0] <= 0:
                    cell.pos = (cell.rows - 1, cell.pos[1])
                if cell.dx == 1 and cell.pos[0] >= cell.rows - 1:
                    cell.pos = (0, cell.pos[1])
                if cell.dy == 1 and cell.pos[1] >= cell.rows - 1:
                    cell.pos = (cell.pos[0], 0)
                if cell.dy == -1 and cell.pos[1] <= 0:
                    cell.pos = (cell.pos[0], cell.rows - 1)
                else:
                    cell.move(cell.dx, cell.dy)

    def draw(self, surface):
        for i, cell in enumerate(self.body):
            cell.draw(surface)

    def add_cell(self):
        tail = self.body[-1]
        dx, dy = tail.dx, tail.dy
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dx, self.body[-1].dy = dx, dy

    def reset(self, pos):
        self.head = Cube(pos, head=True)
        self.body = []
        self.turns = {}
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1


def draw_grid(surface):
    x, y = 0, 0
    for _ in range(ROWS):
        x = x + CELL_SIZE
        y = y + CELL_SIZE
        # Horizontal Line
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, WIDTH))
        # Vertical Line
        pygame.draw.line(surface, (255, 255, 255), (0, y), (WIDTH, y))


def random_food(item):
    positions = item.body

    while True:
        x, y = random.randrange(ROWS), random.randrange(ROWS)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


def redraw_window(surface):
    surface.fill(BG_COLOR)
    snake.draw(surface)
    food.draw(surface)
    # draw_grid(surface)
    pygame.display.update()


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global snake, food
    win = pygame.display.set_mode((WIDTH, WIDTH))
    snake = Snake(SNAKE_COLOR, (10, 10))
    food = Cube(random_food(snake), color=FOOD_COLOR)
    run = True

    clock = pygame.time.Clock()

    while run:
        pygame.time.delay(50)  # the lower the delay the faster the game
        clock.tick(10)  # the lower the time, the slower the game

        snake.move()
        if snake.body[0].pos == food.pos:
            snake.add_cell()
            food = Cube(random_food(snake), color=FOOD_COLOR)

        for x in range(len(snake.body)-2):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x+1:])):
                print(f'Score: {len(snake.body) - 1}')
                message_box("Game Over!", "Play Again...")
                snake.reset((10, 10))
                break
        # Draw the window again
        redraw_window(win)

#
# if "__name__" == "__main__":
#     main()
main()
