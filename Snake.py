import time

import keyboard
import pygame

from Buttons import Buttons


class Snake:
    initial_coordinates_of_the_snake = [[100, 40], [80, 40], [60, 40], [40, 40], [20, 40]]
    coordinates_of_the_snake = [[100, 40], [80, 40], [60, 40], [40, 40], [20, 40]]
    points = ''
    direction = 'right'
    width = 20
    height = 20
    keys = None
    last_moved = 0
    run = True

    def __init__(self, win):
        self.win = win
        self.game_over = pygame.image.load('gameOver2.png').convert_alpha()
        self.game_over = Buttons(200, 300, self.game_over, 1.5, self.win)
        self.font = pygame.font.SysFont(None, 80)

    def render_snake(self):
        for i in range(len(self.coordinates_of_the_snake)):
            pygame.draw.rect(self.win, (0, 255, 0),
                             (self.coordinates_of_the_snake[i][0], self.coordinates_of_the_snake[i][1], self.width,
                              self.height))

    def check_keys(self):
        self.keys = pygame.key.get_pressed()

    def check_direction(self):
        if self.keys[pygame.K_RIGHT] or self.direction == 'right':
            self.direction = 'right'

        if self.keys[pygame.K_LEFT] or self.direction == 'left':
            self.direction = 'left'

        if self.keys[pygame.K_UP] or self.direction == 'up':
            self.direction = 'up'

        if self.keys[pygame.K_DOWN] or self.direction == 'down':
            self.direction = 'down'

    def change_of_snake_position(self):
        if self.last_moved + 0.1 < time.time():
            self.coordinates_of_the_snake.insert(0, self.coordinates_of_the_snake[0].copy())

            self.coordinates_of_the_snake.pop(-1)

            match self.direction:
                case 'left':
                    self.coordinates_of_the_snake[0][0] = self.coordinates_of_the_snake[0][0] - 20
                case 'right':
                    self.coordinates_of_the_snake[0][0] = self.coordinates_of_the_snake[0][0] + 20
                case 'up':
                    self.coordinates_of_the_snake[0][1] = self.coordinates_of_the_snake[0][1] - 20
                case 'down':
                    self.coordinates_of_the_snake[0][1] = self.coordinates_of_the_snake[0][1] + 20

            self.last_moved = time.time()

    def check_collision_with_itself(self):
        for i in range(1, len(self.coordinates_of_the_snake)):
            if self.coordinates_of_the_snake[0] == self.coordinates_of_the_snake[i]:
                self.reset_game()
                self.direction = 'right'
                self.run = True
                break

    def reset_game(self):

        while self.run:
            self.application_closing_service()

            pygame.display.update()
            self.game_over.render_elements()
            self.render_points(2, 3, 'Your points = ')
            pygame.display.update()

            a = keyboard.read_key()
            if a == 'enter':  # reset game
                self.direction = 'right'
                pygame.display.update()
                self.run = False

            elif a == 'esc':  # exit from game
                print("EXIT GAME\n")
                exit(0)
            self.coordinates_of_the_snake = self.initial_coordinates_of_the_snake.copy()
            self.counting_length_of_snake()
            self.points = self.counting_length_of_snake()

    def check_collision_with_walls(self, map_points):
        for i in range(len(map_points)):
            if self.coordinates_of_the_snake[0] == map_points[i]:
                self.reset_game()
                self.direction = 'right'
                self.run = True

    def application_closing_service(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def render_points(self, position_x, position_y, text):

        counting_text = self.font.render(text + self.counting_length_of_snake(), True, (255, 255, 255))
        self.win.blit(counting_text, ((self.win.get_width() - counting_text.get_width()) / position_x,
                                      (self.win.get_height() - counting_text.get_height()) / position_y))

    def run_all_methods(self):
        Snake.check_collision_with_itself(self)
        Snake.render_snake(self)
        Snake.check_keys(self)
        Snake.check_direction(self)
        Snake.change_of_snake_position(self)
        # Snake.counting_length_of_snake(self)

    def counting_length_of_snake(self):
        self.points = str(len(self.coordinates_of_the_snake) - len(self.initial_coordinates_of_the_snake))

        return self.points
