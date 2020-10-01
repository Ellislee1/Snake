import sys
import pygame
import numpy as np
import math

pygame.init()
pygame.display.set_caption('Bad Snake | Score:0 (Press an arrow key to start)')

SIZE = WIDTH, HEIGHT = 380, 240
BOARD_SIZE = B_WIDTH, B_HEIGHT = int(WIDTH / 10), int(HEIGHT/10)
centre = (math.floor(B_WIDTH / 2), math.floor(B_HEIGHT / 2))
SQUARE_SIZE = 10
black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
collect = pygame.mixer.Sound("sounds/puckup.wav")
level = pygame.mixer.Sound("sounds/level.wav")


class Snake:
    def __init__(self, centre):
        self.start = centre
        self.snake = [centre]
        self.symbol = 1
        self.direction = 0
        self.previous_last = centre

    def reset(self):
        self.snake = [self.start]
        self.direction = 0
        self.previous_last = self.start

    def update_snake(self):
        next_seg = self.snake[0]
        if self.direction == 4:
            x, y = self.snake[0]
            y -= 1
            self.snake[0] = (x, y)
        elif self.direction == 3:
            x, y = self.snake[0]
            x += 1
            self.snake[0] = (x, y)
        elif self.direction == 2:
            x, y = self.snake[0]
            y += 1
            self.snake[0] = (x, y)
        elif self.direction == 1:
            x, y = self.snake[0]
            x -= 1
            self.snake[0] = (x, y)

        if len(self.snake) > 1:
            for i in range(1, len(self.snake)):
                temp = self.snake[i]
                self.snake[i] = next_seg
                next_seg = temp

    def get_collision(self, board):
        y, x = self.snake[0]

        if x >= 0 and x < board.height:
            if y >= 0 and y < board.width:
                pass
            else:
                return False
        else:
            return False

        if len(self.snake) > 1:
            for i in range(0, len(self.snake)-1):
                x = self.snake[i]
                for j in range(i+1, len(self.snake)):
                    y = self.snake[j]
                    if x == y:
                        return False

        return True

    def add(self):
        self.snake.append(self.previous_last)

    def update_last(self):
        self.previous_last = self.snake[-1]


class Board:
    def __init__(self, Width, Height):
        self.width = Width
        self.height = Height
        self.board = np.zeros([self.width, self.height], dtype=int)
        self.food = (0, 0)
        self.score = 0
        self.high_score = 0

    def reset(self, snake):
        self.board = np.zeros([self.width, self.height], dtype=int)
        self.food = (0, 0)
        self.score = 0
        self.add_snake(snake)
        self.add_food()

    def print_board(self):
        print(self.board)

    def add_snake(self, snake):
        for space in snake.snake:
            x, y = space
            self.board[x, y] = snake.symbol

    def add_food(self):
        while 1:
            (x, y) = np.random.randint(self.width), np.random.randint(self.height)

            if self.board[x, y] == 0:
                self.board[x, y] = 2
                self.food = (x, y)
                return

    def update_board(self, snake):
        snake.update_snake()
        if not snake.get_collision(self):
            print(f'Score: {self.score}')
            return False

        if snake.snake[0] == self.food:
            snake.add()
            self.score += 1
            self.add_food()
            if self.score > self.high_score:
                self.high_score = self.score
            if (self.score % 10 == 0):
                pygame.mixer.Sound.play(level)
            else:
                pygame.mixer.Sound.play(collect)
            pygame.display.set_caption(
                f'Bad Snake | Score:{self.score} | High Score: {self.high_score}')

        self.board = np.zeros([self.width, self.height], dtype=int)
        self.add_snake(snake)
        x, y = self.food
        self.board[x, y] = 2
        snake.update_last()
        return True


def draw_game(screen, board):
    grid = board.board

    for i in range(0, B_WIDTH):
        for j in range(0, B_HEIGHT):
            if grid[i, j] == 1:
                pygame.draw.rect(
                    screen, green, [10 * i, 10 * j, SQUARE_SIZE, SQUARE_SIZE])
            elif grid[i, j] == 2:
                pygame.draw.rect(
                    screen, red, [10 * i, 10 * j, SQUARE_SIZE, SQUARE_SIZE])


def main():
    snake = Snake(centre)
    board = Board(B_WIDTH, B_HEIGHT)

    board.add_snake(snake)
    board.add_food()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = True
    game_start = False
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                if event.key == pygame.K_RIGHT:
                    if not snake.direction == 1:
                        snake.direction = 3
                        game_start = True
                if event.key == pygame.K_DOWN:
                    if not snake.direction == 4:
                        snake.direction = 2
                        game_start = True
                if event.key == pygame.K_LEFT:
                    if not snake.direction == 3:
                        snake.direction = 1
                        game_start = True
                if event.key == pygame.K_UP:
                    if not snake.direction == 2:
                        snake.direction = 4
                        game_start = True

        screen.fill(black)
        draw_game(screen, board)
        # board.print_board()
        # direction = input("press enter")
        # snake.direction = int(direction)
        pygame.display.update()
        if game_start:
            if (not board.update_board(snake)):
                snake.reset()
                board.reset(snake)
                game_start = False
        pygame.time.wait(75)


main()
