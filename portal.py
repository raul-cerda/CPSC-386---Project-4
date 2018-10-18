# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Pacman Portal
import pygame


class Portal(pygame.sprite.Sprite):

    def __init__(self, screen, portal_color):
        super(Portal, self).__init__()
        self.screen = screen
        self.images = [pygame.image.load('images/bportal.png'), pygame.image.load('images/oportal.png')]
        if portal_color == 'blue':
            self.color = 0
        else:
            self.color = 1
        self.image = self.images[self.color]
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
