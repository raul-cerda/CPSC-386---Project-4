# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Pacman Portal
import pygame


class Pacman(pygame.sprite.Sprite):

    def __init__(self, screen, maze):
        super(Pacman, self).__init__()
        self.screen = screen
        self.maze = maze

        self.img_list = [[]]
        self.death_imgs = []
        self.image = pygame.Surface((100, 100))
        sheet = pygame.image.load('images/pacfull.png')

        self.image.set_colorkey((0, 0, 0))
        self.image.blit(sheet, (0, 0), (0, 0, 100, 100))
        self.image = pygame.transform.scale(self.image, (33, 33))
        self.rect = self.image.get_rect()

        for i in range(0, 4):
            for j in range(0, 4):
                temp_img = pygame.Surface((100, 100))
                temp_img.set_colorkey((0, 0, 0))
                temp_img.blit(sheet, (0, 0), (i*100, j*100, 100, 100))
                temp = pygame.transform.scale(temp_img, (33, 33))
                self.img_list[i].append(temp)
            self.img_list.append([])

        for i in range(0, 10):
            temp_img = pygame.Surface((100, 100))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (400, i * 100, 100, 100))
            temp = pygame.transform.scale(temp_img, (33, 33))
            self.death_imgs.append(temp)

        self.imgx = 0
        self.imgy = 0

        self.current_dir = 0
        self.is_teleporting = 0
        self.dying = False
        self.death_frame_counter = 0
        self.powered_up = False
        self.ghost_pt_mult = 1
        self.power_timer = 0

    def blitme(self):
        if not self.dying:
            if self.imgy < 18:
                self.imgy += 1
            else:
                self.imgy = 0
            self.image = self.img_list[self.imgx][int(self.imgy / 5)]
        else:
            if self.death_frame_counter < 100:
                self.image = self.death_imgs[int(self.death_frame_counter / 10)]
                self.death_frame_counter += 1
            else:
                self.dying = False
                self.death_frame_counter = 0
        self.screen.blit(self.image, self.rect)

    def move(self):
        if self.ghost_pt_mult == 5:
            self.ghost_pt_mult = 1
        if self.power_timer < 500 and self.powered_up:
            self.power_timer += 1
        elif self.powered_up:
            self.powered_up = False
            self.power_timer = 0

        if self.current_dir == 1 and self.maze.front_path_is_clear(1, self):
            self.rect.y -= 2
        if self.current_dir == 3 and self.maze.front_path_is_clear(3, self):
            self.rect.y += 2
        if self.current_dir == 4 and self.maze.front_path_is_clear(4, self):
            self.rect.x -= 2
        if self.current_dir == 2 and self.maze.front_path_is_clear(2, self):
            self.rect.x += 2

    def moveup(self):
        if self.maze.front_path_is_clear(1, self):
            self.current_dir = 1
            self.imgx = 0

    def movedown(self):
        if self.maze.front_path_is_clear(3, self):
            self.current_dir = 3
            self.imgx = 2

    def moveleft(self):
        if self.maze.front_path_is_clear(4, self):
            self.current_dir = 4
            self.imgx = 3

    def moveright(self):
        if self.maze.front_path_is_clear(2, self):
            self.current_dir = 2
            self.imgx = 1

    def pac_dot_in_front(self):
        obj_pos = self.maze.get_obj_pos(self)
        if self.current_dir == 1:
            return self.maze.rows[obj_pos[1]][obj_pos[0] + 1] == '.'
        if self.current_dir == 2:
            return self.maze.rows[obj_pos[1] + 1][obj_pos[0] + 3] == '.'
        if self.current_dir == 3:
            return self.maze.rows[obj_pos[1] + 3][obj_pos[0] + 1] == '.'
        if self.current_dir == 4:
            return self.maze.rows[obj_pos[1] + 1][obj_pos[0]] == '.'

    def find_portal_spot(self):
        if self.current_dir == 1:
            x = self.rect.centerx
            y = self.rect.y
            while self.screen.get_at((x, y)) != (36, 28, 252):
                y -= 2
            return x, y + 17
        if self.current_dir == 2:
            x = self.rect.x
            y = self.rect.centery
            while self.screen.get_at((x, y)) != (36, 28, 252):
                x += 2
            return x - 17, y
        if self.current_dir == 3:
            x = self.rect.centerx
            y = self.rect.y
            while self.screen.get_at((x, y)) != (36, 28, 252):
                y += 2
            return x, y - 17
        if self.current_dir == 4:
            x = self.rect.x
            y = self.rect.centery
            while self.screen.get_at((x, y)) != (36, 28, 252):
                x -= 2
            return x + 17, y

    def die(self):
        self.dying = True
