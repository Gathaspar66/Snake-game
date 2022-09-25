import random

import keyboard
import pygame

from Snake import Snake


class LevelManager:
    map = []
    width = 19
    height = 19
    x_in_food = 60
    y_in_food = 60
    number_of_level = ''

    def __init__(self, win):
        self.win = win
        self.snake = Snake(self)

    def map_render(self):

        for i in range(len(self.map)):
            a = random.randrange(0, 255, 1)
            b = random.randrange(0, 100, 1)

            match self.number_of_level:
                case 'level1.txt':
                    pygame.draw.rect(self.win, (a, 255, 255),
                                     (int(self.map[i][0]), int(self.map[i][1]), self.width + 1, self.height + 1))
                case 'level2.txt':
                    pygame.draw.rect(self.win, (100, b, 200),
                                     (int(self.map[i][0]), int(self.map[i][1]), self.width + 1, self.height + 1))
                case 'level3.txt':
                    pygame.draw.rect(self.win, (255, 255, a),
                                     (int(self.map[i][0]), int(self.map[i][1]), self.width + 1, self.height + 1))

                case 'level4.txt':
                    pygame.draw.rect(self.win, (b, 255, a),
                                     (int(self.map[i][0]), int(self.map[i][1]), self.width + 1, self.height + 1))

    def check_eating(self, coordinates_of_the_snake):

        if self.x_in_food == coordinates_of_the_snake[0][0] and self.y_in_food == coordinates_of_the_snake[0][1]:
            coordinates_of_the_snake.insert(-1, coordinates_of_the_snake[-1].copy())
            self.draw_food_items()

        pygame.draw.circle(self.win, (255, 0, 0), (self.x_in_food + 10, self.y_in_food + 10), 5)

    def draw_food_items(self):
        self.x_in_food = random.randrange(0, 1000, 20)
        self.y_in_food = random.randrange(0, 1000, 20)
        for i in range(len(self.map)):

            if self.map[i][0] == self.x_in_food and self.map[i][1] == self.y_in_food:
                self.draw_food_items()

    def increasing_snake_length(self, coordinates_of_the_snake):
        coordinates_of_the_snake.insert(-1, coordinates_of_the_snake[-1].copy())

    def load_map(self, number_of_level):
        self.number_of_level = number_of_level
        self.map.clear()

        file = open(number_of_level, 'r')
        text = file.read()

        x = text.split(";")
        x.pop(-1)

        for i in x:
            temp = i.split(','.rstrip())

            if temp[2] == '1':
                temp.pop(-1)
                temp = list(map(int, temp))
                temp[0] = temp[0] * 20
                temp[1] = temp[1] * 20
                self.map.append(temp)

        file.close()


