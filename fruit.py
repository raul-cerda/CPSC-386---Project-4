# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Pacman Portal
import pygame


class Fruit(pygame.sprite.Sprite):

    def __init__(self, screen, fruit_num):
        super(Fruit, self).__init__()
        self.screen = screen
        sheet = pygame.image.load('images/fruitsheet.png')
        self.fruits = []
        for i in range(0, 8):
            temp_img = pygame.Surface((100, 100))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (0, i * 50, 50, 50))
            temp = pygame.transform.scale(temp_img, (60, 60))
            self.fruits.append(temp)

        self.image = self.fruits[fruit_num]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.visible = False
        self.visible_counter = 0

    def blitme(self):
        if self.visible:
            self.screen.blit(self.image, self.rect)

    def set_invisible(self):
        if self.visible_counter < 500 and self.visible:
            self.visible_counter += 1
        elif self.visible:
            self.visible = False
            self.rect.x = 0
            self.rect.y = 0
            self.visible_counter = 0

    def show_self(self):
        self.visible = True
        self.rect.x = 297
        self.rect.y = 462
        self.set_invisible()
