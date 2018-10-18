# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Pacman Portal
import pygame


class Animation:
    def __init__(self, screen, maze):
        self.screen = screen
        self.maze = maze
        self.img_list = [pygame.image.load('images/chase1.png'), pygame.image.load('images/chase2.png'),
                         pygame.image.load('images/chase3.png'), pygame.image.load('images/chase4.png')]
        self.image = self.img_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 350

        self.super_img = pygame.image.load("images/ghostnames.png")
        self.super_rect = self.super_img.get_rect()
        self.super_rect.y = 350

        self.current_frame = 0
        self.right = 0

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.rect.x <= 650 and self.right == 0:
            self.update_right()
        elif self.right == 0:
            self.right = 1
            self.current_frame = 60
        if self.right == 1:
            self.update_left()
        if self.right == 1 and self.rect.x < 0:
            self.right = 2
            self.update_center()

    def update_center(self):
        self.image = self.super_img
        self.rect = self.super_rect

    def update_right(self):
        if self.current_frame < 59:
            self.current_frame += 1
        else:
            self.current_frame = 0
        self.image = self.img_list[int(self.current_frame / 30)]
        self.rect.x += 2

    def update_left(self):
        if self.current_frame < 119:
            self.current_frame += 1
        else:
            self.current_frame = 60
        self.image = self.img_list[int(self.current_frame / 30)]
        self.rect.x -= 2
