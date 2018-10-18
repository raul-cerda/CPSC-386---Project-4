# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Pacman Portal
import pygame
from random import randint


class Ghost(pygame.sprite.Sprite):

    def __init__(self, screen, maze, ghost_name):
        super(Ghost, self).__init__()
        self.screen = screen
        self.maze = maze
        self.enemy = self.maze.pac_man
        self.ghost_name = ghost_name

        self.img_list = [[]]
        self.image = pygame.Surface((100, 100))
        sheet = pygame.image.load('images/ghosts.png')

        self.image.set_colorkey((0, 0, 0))
        self.image.blit(sheet, (0, 0), (0, 0, 100, 100))
        self.image = pygame.transform.scale(self.image, (33, 33))
        self.rect = self.image.get_rect()

        for i in range(0, 4):
            for j in range(0, 8):
                temp_img = pygame.Surface((100, 100))
                temp_img.set_colorkey((0, 0, 0))
                temp_img.blit(sheet, (0, 0), (i * 125, j * 125, 100, 100))
                temp = pygame.transform.scale(temp_img, (33, 33))
                self.img_list[i].append(temp)
            self.img_list.append([])
        for i in range(0, 2):
            temp_img = pygame.Surface((100, 100))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (500, i * 125, 100, 100))
            temp = pygame.transform.scale(temp_img, (33, 33))
            self.img_list[4].append(temp)

        if self.ghost_name == 'blinky':
            self.imgx = 0
        elif self.ghost_name == 'pinky':
            self.imgx = 1
        elif self.ghost_name == 'inky':
            self.imgx = 2
        else:
            self.imgx = 3
        self.imgy = 0

        self.frame_counter = 0
        self.current_dir = 1
        self.scared = False
        self.scared_timer = 0

        self.is_teleporting = 0

    def blitme(self):
        if not self.scared:
            if self.frame_counter <= 30:
                self.image = self.img_list[self.imgx][self.imgy]
                self.frame_counter += 1
            elif self.frame_counter <= 60:
                self.image = self.img_list[self.imgx][self.imgy + 4]
                self.frame_counter += 1
            else:
                self.frame_counter = 0
        else:
            if self.scared_timer < 400:
                self.image = self.img_list[4][0]
            else:
                if self.frame_counter <= 30:
                    self.image = self.img_list[4][0]
                    self.frame_counter += 1
                elif self.frame_counter <= 60:
                    self.image = self.img_list[4][1]
                    self.frame_counter += 1
                else:
                    self.frame_counter = 0
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.scared and self.scared_timer < 400:
            self.scared_timer += 1
        elif self.scared and self.scared_timer < 500:
            self.scared_timer += 1
        elif self.scared:
            self.scared = False
            self.scared_timer = 0

        if self.imgx == 0:
            self.update_blinky()
        elif self.imgx == 1:
            self.update_pinky()
        elif self.imgx == 2:
            self.update_inky()
        elif self.imgx == 3:
            self.update_clyde()

        if self.is_teleporting != 0:
            self.is_teleporting += 1
        if self.is_teleporting >= 100:
            self.is_teleporting = 0

    def move(self):
        if self.current_dir == 1 and self.maze.front_path_is_clear(1, self):
            self.rect.y -= 2
        if self.current_dir == 3 and self.maze.front_path_is_clear(3, self):
            self.rect.y += 2
        if self.current_dir == 4 and self.maze.front_path_is_clear(4, self):
            self.rect.x -= 2
        if self.current_dir == 2 and self.maze.front_path_is_clear(2, self):
            self.rect.x += 2

    def update_blinky(self):
        if self.current_dir == 1 and not self.maze.front_path_is_clear(1, self):
            if self.enemy.rect.x < self.rect.x:
                if self.maze.left_is_clear(self):
                    self.moveleft()
                elif self.maze.right_is_clear(self):
                    self.moveright()
            else:
                if self.maze.right_is_clear(self):
                    self.moveright()
                elif self.maze.left_is_clear(self):
                    self.moveleft()

        elif self.current_dir == 2 and not self.maze.front_path_is_clear(2, self):
            if self.enemy.rect.y < self.rect.y:
                if self.maze.top_is_clear(self):
                    self.moveup()
                elif self.maze.bot_is_clear(self):
                    self.movedown()
            else:
                if self.maze.bot_is_clear(self):
                    self.movedown()
                elif self.maze.top_is_clear(self):
                    self.moveup()

        elif self.current_dir == 3 and not self.maze.front_path_is_clear(3, self):
            if self.enemy.rect.x < self.rect.x:
                if self.maze.left_is_clear(self):
                    self.moveleft()
                elif self.maze.right_is_clear(self):
                    self.moveright()
            else:
                if self.maze.right_is_clear(self):
                    self.moveright()
                elif self.maze.left_is_clear(self):
                    self.moveleft()

        elif self.current_dir == 4 and not self.maze.front_path_is_clear(4, self):
            if self.enemy.rect.y < self.rect.y:
                if self.maze.top_is_clear(self):
                    self.moveup()
                elif self.maze.bot_is_clear(self):
                    self.movedown()
            else:
                if self.maze.bot_is_clear(self):
                    self.movedown()
                elif self.maze.top_is_clear(self):
                    self.moveup()
        else:
            self.move()

    def update_pinky(self):
        if self.current_dir == 1 and not self.maze.front_path_is_clear(1, self):
            if self.maze.left_is_clear(self):
                self.moveleft()
            elif self.maze.right_is_clear(self):
                self.moveright()

        elif self.current_dir == 2 and not self.maze.front_path_is_clear(2, self):
            if self.maze.top_is_clear(self):
                self.moveup()
            elif self.maze.bot_is_clear(self):
                self.movedown()

        elif self.current_dir == 3 and not self.maze.front_path_is_clear(3, self):
            if self.maze.left_is_clear(self):
                self.moveleft()
            elif self.maze.right_is_clear(self):
                self.moveright()

        elif self.current_dir == 4 and not self.maze.front_path_is_clear(4, self):
            if self.maze.top_is_clear(self):
                self.moveup()
            elif self.maze.bot_is_clear(self):
                self.movedown()
        else:
            self.move()

    def update_inky(self):
        if self.current_dir == 1 and not self.maze.front_path_is_clear(1, self):
            if self.maze.right_is_clear(self):
                self.moveright()
            elif self.maze.left_is_clear(self):
                self.moveleft()

        elif self.current_dir == 2 and not self.maze.front_path_is_clear(2, self):
            if self.maze.bot_is_clear(self):
                self.movedown()
            elif self.maze.top_is_clear(self):
                self.moveup()

        elif self.current_dir == 3 and not self.maze.front_path_is_clear(3, self):
            if self.maze.right_is_clear(self):
                self.moveright()
            elif self.maze.left_is_clear(self):
                self.moveleft()

        elif self.current_dir == 4 and not self.maze.front_path_is_clear(4, self):
            if self.maze.bot_is_clear(self):
                self.movedown()
            elif self.maze.top_is_clear(self):
                self.moveup()
        else:
            self.move()

    def update_clyde(self):
        decision = randint(0, 1)
        if self.current_dir == 1 and not self.maze.front_path_is_clear(1, self):
            if self.maze.right_is_clear(self) and self.maze.left_is_clear(self):
                if decision == 0:
                    self.moveright()
                else:
                    self.moveleft()
            elif self.maze.right_is_clear(self):
                self.moveright()
            elif self.maze.left_is_clear(self):
                self.moveleft()

        elif self.current_dir == 2 and not self.maze.front_path_is_clear(2, self):
            if self.maze.bot_is_clear(self) and self.maze.top_is_clear(self):
                if decision == 0:
                    self.movedown()
                else:
                    self.moveup()
            elif self.maze.bot_is_clear(self):
                self.movedown()
            elif self.maze.top_is_clear(self):
                self.moveup()

        elif self.current_dir == 3 and not self.maze.front_path_is_clear(3, self):
            if self.maze.right_is_clear(self) and self.maze.left_is_clear(self):
                if decision == 0:
                    self.moveright()
                else:
                    self.moveleft()
            elif self.maze.right_is_clear(self):
                self.moveright()
            elif self.maze.left_is_clear(self):
                self.moveleft()

        elif self.current_dir == 4 and not self.maze.front_path_is_clear(4, self):
            if self.maze.bot_is_clear(self) and self.maze.top_is_clear(self):
                if decision == 0:
                    self.movedown()
                else:
                    self.moveup()
            elif self.maze.bot_is_clear(self):
                self.movedown()
            elif self.maze.top_is_clear(self):
                self.moveup()
        else:
            self.move()

    def moveup(self):
        if self.maze.front_path_is_clear(1, self):
            self.current_dir = 1
            self.imgy = 0

    def movedown(self):
        if self.maze.front_path_is_clear(3, self):
            self.current_dir = 3
            self.imgy = 2

    def moveleft(self):
        if self.maze.front_path_is_clear(4, self):
            self.current_dir = 4
            self.imgy = 3

    def moveright(self):
        if self.maze.front_path_is_clear(2, self):
            self.current_dir = 2
            self.imgy = 1

    def return_to_center(self):
        self.rect.x = 298
        self.rect.y = 254
        self.current_dir = 1
