import pygame

from Buttons import Buttons
from LevelManager import LevelManager
from Snake import Snake


class GameManager:
    screen_size = 1000
    run = True
    application_mode = 'menu'
    keys = None
    text = ''
    status = False
    time_elapsed_since_last_action = 0
    clock = pygame.time.Clock()
    def __init__(self):  # Initialization of objects displayed in the game.
        pygame.init()
        self.win = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Pierwsza gra \"WUNSZ\"")

        self.start_img = pygame.image.load('button_start.png').convert_alpha()
        self.exit_img = pygame.image.load('button_exit.png').convert_alpha()
        self.logo = pygame.image.load('Wynsz_the_game_logo.png').convert_alpha()
        self.level1 = pygame.image.load('button_level1.png').convert_alpha()
        self.level2 = pygame.image.load('button_level2.png').convert_alpha()
        self.level3 = pygame.image.load('button_level3.png').convert_alpha()
        self.level4 = pygame.image.load('button_level4.png').convert_alpha()
        self.restart = pygame.image.load('button_restart.png').convert_alpha()
        self.continue_playing = pygame.image.load('button_continue.png').convert_alpha()
        self.level_selection_button = pygame.image.load('button_level-selection.png').convert_alpha()

        self.level_walls = LevelManager(self.win)
        self.snake = Snake(self.win)

        self.logo = Buttons(0, 0, self.logo, 1, self.win)
        self.level1 = Buttons(100, 300, self.level1, 1, self.win)
        self.level2 = Buttons(300, 300, self.level2, 1, self.win)
        self.level3 = Buttons(500, 300, self.level3, 1, self.win)
        self.level4 = Buttons(700, 300, self.level4, 1, self.win)

        self.start = Buttons(200, 500, self.start_img, 1, self.win)
        self.exit = Buttons(600, 500, self.exit_img, 1, self.win)
        self.restart = Buttons(400, 100, self.restart, 1, self.win)
        self.continue_playing = Buttons(395, 300, self.continue_playing, 1, self.win)
        self.level_selection_button = Buttons(365, 500, self.level_selection_button, 1, self.win)

        self.game_mode_adjustment()

    def game_mode_adjustment(self):  # Setup of the appropriate part of the program.

        while self.run:
            self.application_closing_service()

            match self.application_mode:
                case 'menu':
                    GameManager.menu_handling(self)
                case 'level selection':
                    GameManager.level_selection_handling(self)
                case 'game':
                    GameManager.game_handling(self)
                case 'game_survival':
                    GameManager.game_survival_handling(self)
                case 'pause':
                    GameManager.pause_handling(self)

    def menu_handling(self):
        while self.run:

            self.application_closing_service()
            self.logo.render_elements()
            self.start.render_elements()
            self.exit.render_elements()

            if self.start.check_if_clicked():
                self.win.fill((0, 0, 0))
                self.application_mode = 'level selection'
                break
            if self.exit.check_if_clicked():
                exit(0)
            pygame.display.update()

    def level_selection_handling(self):

        while self.run:
            pygame.display.flip()
            self.win.fill((0, 0, 0))
            self.application_closing_service()
            self.level1.render_elements()
            self.level2.render_elements()
            self.level3.render_elements()
            self.level4.render_elements()

            if self.level1.check_if_clicked():
                Snake.coordinates_of_the_snake = Snake.initial_coordinates_of_the_snake.copy()
                self.application_mode = 'game'
                self.level1.clicked = False
                self.level_walls.load_map('level1.txt')
                break

            if self.level2.check_if_clicked():
                Snake.coordinates_of_the_snake = Snake.initial_coordinates_of_the_snake.copy()
                self.application_mode = 'game'
                self.level2.clicked = False
                self.level_walls.load_map('level2.txt')
                break

            if self.level3.check_if_clicked():
                Snake.coordinates_of_the_snake = Snake.initial_coordinates_of_the_snake.copy()
                self.application_mode = 'game'
                self.level3.clicked = False
                self.level_walls.load_map('level3.txt')
                break

            if self.level4.check_if_clicked():
                Snake.coordinates_of_the_snake = Snake.initial_coordinates_of_the_snake.copy()
                self.application_mode = 'game_survival'
                self.level4.clicked = False
                self.level_walls.load_map('level4.txt')
                break

    def game_handling(self):
        while self.run:
            self.win.fill((0, 0, 0))
            self.level_walls.map_render()
            self.snake.render_points(1.050, 30, self.text)
            self.snake.run_all_methods()

            self.snake.check_collision_with_walls(self.level_walls.map)
            self.level_walls.check_eating(self.snake.coordinates_of_the_snake)

            pygame.display.flip()

            self.check_keys()
            if self.check_esc_is_clicked():
                self.application_mode = 'pause'
                break
            self.application_closing_service()

    def game_survival_handling(self):
        self.status = True
        self.time_elapsed_since_last_action = 0

        while self.run:
            self.win.fill((0, 0, 0))
            self.level_walls.map_render()
            self.snake.run_all_methods()
            self.snake.check_collision_with_walls(self.level_walls.map)

            dt = self.clock.tick()
            self.time_elapsed_since_last_action += dt

            if self.time_elapsed_since_last_action > 1000:
                self.level_walls.increasing_snake_length(self.snake.coordinates_of_the_snake)
                self.time_elapsed_since_last_action = 0

            self.snake.render_points(1.050, 30, self.text)

            pygame.display.flip()

            self.check_keys()
            if self.check_esc_is_clicked():
                self.application_mode = 'pause'
                break
            self.application_closing_service()

    def pause_handling(self):
        while self.run:
            self.application_closing_service()
            self.win.fill((0, 0, 0))

            self.restart.render_elements()
            self.level_selection_button.render_elements()
            self.continue_playing.render_elements()

            if self.restart.check_if_clicked():

                if self.status is False:
                    self.application_mode = 'game'
                else:
                    self.application_mode = 'game_survival'

                self.snake.coordinates_of_the_snake = self.snake.initial_coordinates_of_the_snake.copy()
                break
            if self.level_selection_button.check_if_clicked():
                self.application_mode = 'level selection'
                self.status = False
                self.snake.coordinates_of_the_snake = self.snake.initial_coordinates_of_the_snake.copy()
                break

            if self.continue_playing.check_if_clicked():
                if self.status is False:
                    self.application_mode = 'game'
                else:
                    self.application_mode = 'game_survival'

                break

            pygame.display.flip()

    def application_closing_service(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def check_keys(self):
        self.keys = pygame.key.get_pressed()

    def check_esc_is_clicked(self):
        if self.keys[pygame.K_ESCAPE]:
            return True


game = GameManager()
