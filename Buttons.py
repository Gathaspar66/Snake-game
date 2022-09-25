import pygame


class Buttons:

    def __init__(self, x, y, image, scale, win):
        self.clicked = False
        self.x = x
        self.y = y
        self.win = win
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def check_if_clicked(self):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return self.clicked

    def render_elements(self):
        self.win.blit(self.image, (self.x, self.y))
