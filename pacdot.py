# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Pacman Portal
import pygame


class Pacdot(pygame.sprite.Sprite):

    def __init__(self, screen, dot_image):
        super(Pacdot, self).__init__()
        self.screen = screen
        self.image = dot_image
        self.rect = pygame.Rect(0, 0, 0, 0)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def spawn(self):
        return Pacdot(self.screen, self.image)
