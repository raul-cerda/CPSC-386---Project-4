import pygame
import time
from imageRect import Image
from pacman import Pacman
from ghost import Ghost
from pacdot import Pacdot
from fruit import Fruit
from button import Button
from portal import Portal
from animation import Animation
import sys


class Maze:
    BRICK_SIZE = 11

    def __init__(self, screen, mazefile, stats, clock):
        self.screen = screen
        self.stats = stats
        self.clock = clock
        self.radio = pygame.mixer
        self.radio.init()
        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.maze_obj = []
        size = Maze.BRICK_SIZE
        self.brick = Image(screen, 'brick', size, size)

        self.default_ports = pygame.sprite.Group()
        self.def_port_list = []
        self.lport = Portal(self.screen, 'blue')
        self.rport = Portal(self.screen, 'orange')

        self.pac_dots = pygame.sprite.Group()
        self.pac_dot = Pacdot(screen, pygame.image.load('images/pacdot.png'))
        self.pac_dot.image = pygame.transform.scale(self.pac_dot.image, (8, 8))

        self.power_dots = pygame.sprite.Group()
        self.power = Pacdot(screen, pygame.image.load('images/pacdot.png'))
        self.power.image = pygame.transform.scale(self.power.image, (15, 15))

        self.shield = Image(screen, 'shield', size, size)
        self.pac_man = Pacman(screen, self)
        self.blinky = Ghost(screen, self, 'blinky')
        self.pinky = Ghost(screen, self, 'pinky')
        self.inky = Ghost(screen, self, 'inky')
        self.clyde = Ghost(screen, self, 'clyde')
        self.ghosts = pygame.sprite.Group()
        self.fruit = None
        self.fruits = pygame.sprite.Group()

        self.deltax = self.deltay = Maze.BRICK_SIZE

        # used for menu purposes
        self.title = None
        self.title_rect = None
        self.start_button = None
        self.scores_button = None
        # end of menu items

        # used for sounds
        self.intro = self.radio.Sound('sounds/intro.wav')
        self.ambient = self.radio.Sound('sounds/ambient.wav')
        self.eatdot = self.radio.Sound('sounds/eatdot.wav')
        self.eatghost = self.radio.Sound('sounds/eatghost.wav')
        self.powersound = self.radio.Sound('sounds/power.wav')
        self.death = self.radio.Sound('sounds/death.wav')
        self.gameover = self.radio.Sound('sounds/gameover.wav')

        self.ambient_playing = False
        self.power_playing = False
        # end of sounds

        self.lives_counter = pygame.sprite.Group()
        self.lives_sprites = []

        self.active_ports = pygame.sprite.Group()
        self.bport = None
        self.oport = None
        self.blue_active = False
        self.orange_active = False

        self.build()

    def build(self):
        w, h = Maze.BRICK_SIZE, Maze.BRICK_SIZE
        dx, dy = self.deltax, self.deltay
        self.fruit = Fruit(self.screen, self.stats.current_level)
        self.fruits.add(self.fruit)
        for i in range(0, self.stats.lives):
            temp = Pacman(self.screen, self)
            temp.rect.y = 650
            temp.rect.x = i * 30
            self.lives_counter.add(temp)
            self.lives_sprites.append(temp)

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                current_rect = pygame.Rect(ncol * dx, nrow * dy, w, h)
                if col == 'X':
                    self.maze_obj.append(('brick', current_rect))
                elif col == '.':
                    temp = self.pac_dot.spawn()
                    temp.rect = current_rect
                    self.maze_obj.append(('pacdot', temp))
                    self.pac_dots.add(temp)
                elif col == 'M':
                    self.pac_man.rect.x = current_rect.x - 11
                    self.pac_man.rect.y = current_rect.y - 11
                    self.maze_obj.append(('pacman', self.pac_man.rect))
                elif col == 'P':
                    temp = self.power.spawn()
                    temp.rect = current_rect
                    temp.rect.x -= 3
                    temp.rect.y -= 3
                    self.maze_obj.append(('power', current_rect))
                    self.power_dots.add(temp)
                elif col == 'S':
                    self.maze_obj.append(('shield', current_rect))
                elif col == '1':
                    self.blinky.rect.x = current_rect.x - 10
                    self.blinky.rect.y = current_rect.y - 10
                    self.maze_obj.append(('blinky', self.blinky.rect))
                    self.ghosts.add(self.blinky)
                elif col == '2':
                    self.pinky.rect.x = current_rect.x - 10
                    self.pinky.rect.y = current_rect.y - 10
                    self.maze_obj.append(('pinky', self.pinky.rect))
                    self.ghosts.add(self.pinky)
                elif col == '3':
                    self.inky.rect.x = current_rect.x - 10
                    self.inky.rect.y = current_rect.y - 10
                    self.maze_obj.append(('inky', self.inky.rect))
                    self.ghosts.add(self.inky)
                elif col == '4':
                    self.clyde.rect.x = current_rect.x - 10
                    self.clyde.rect.y = current_rect.y - 10
                    self.maze_obj.append(('clyde', self.clyde.rect))
                    self.ghosts.add(self.clyde)
                elif col == 'B':
                    self.lport.rect = current_rect
                    self.maze_obj.append(('port1', self.lport.rect))
                    self.default_ports.add(self.lport)
                    self.def_port_list.append(self.lport)
                elif col == 'O':
                    self.rport.rect = current_rect
                    self.maze_obj.append(('port2', self.rport.rect))
                    self.default_ports.add(self.rport)
                    self.def_port_list.append(self.rport)

    def blitme(self):
        self.pac_dots.draw(self.screen)
        self.power_dots.draw(self.screen)
        self.default_ports.draw(self.screen)
        for obj in self.maze_obj:
            if obj[0] == 'brick':
                self.screen.blit(self.brick.image, obj[1])
            elif obj[0] == 'shield':
                self.screen.blit(self.shield.image, obj[1])
        self.stats.blitme()

    @staticmethod
    def check_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.top_is_clear(self.pac_man):
            self.pac_man.moveup()
        if keys[pygame.K_DOWN] and self.bot_is_clear(self.pac_man):
            self.pac_man.movedown()
        if keys[pygame.K_LEFT] and self.left_is_clear(self.pac_man):
            self.pac_man.moveleft()
        if keys[pygame.K_RIGHT] and self.right_is_clear(self.pac_man):
            self.pac_man.moveright()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.new_high_score(self.stats.current_score)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.fire_blue_portal()
                if event.key == pygame.K_e:
                    self.fire_orange_portal()
                if event.key == pygame.K_SPACE:
                    self.active_ports.empty()
                    self.blue_active = False
                    self.orange_active = False

    def update(self):
        self.check_events(self)
        self.screen.fill((0, 0, 0))
        self.blitme()
        self.dot_eating()
        self.pac_portal_collision()
        self.pac_active_portal_collision()
        self.pac_ghost_collision()
        self.ghost_active_portal_collision()
        if self.stats.game_status == 0:
            return
        if self.pac_man.ghost_pt_mult == 5:
            self.fruit.show_self()
        if not self.pac_man.dying:
            self.pac_man.move()
            self.ghosts.update()
            if self.pac_man.powered_up and not self.power_playing:
                self.ambient.stop()
                self.ambient_playing = False
                self.powersound.play(-1)
                self.power_playing = True
            elif not self.pac_man.powered_up and self.power_playing:
                self.powersound.stop()
                self.power_playing = False
            elif not self.pac_man.powered_up and not self.ambient_playing:
                self.ambient.play(-1)
                self.ambient_playing = True
        else:
            self.ambient.stop()
            self.ambient_playing = False
        self.fruit.set_invisible()
        if self.stats.game_status == 1:
            self.fruits.draw(self.screen)
            self.active_ports.draw(self.screen)
            self.pac_man.blitme()
            self.blinky.blitme()
            self.pinky.blitme()
            self.inky.blitme()
            self.clyde.blitme()
            self.lives_counter.draw(self.screen)

    def dot_eating(self):
        dot_collisions = pygame.sprite.spritecollideany(self.pac_man, self.pac_dots)
        if dot_collisions:
            dot_collisions.kill()
            self.stats.current_score += 10
            self.eatdot.play()
        dot_collisions = pygame.sprite.spritecollideany(self.pac_man, self.power_dots)
        if dot_collisions:
            dot_collisions.kill()
            self.stats.current_score += 50
            self.pac_man.powered_up = True
            for ghost in self.ghosts:
                ghost.scared = True
        if len(self.pac_dots) == 0 and len(self.power_dots) == 0:
            pygame.time.wait(1000)
            self.new_level()
        fruit_collision = pygame.sprite.spritecollideany(self.pac_man, self.fruits)
        if fruit_collision:
            self.stats.current_score += 1000
            self.eatghost.play()
            fruit_collision.kill()
            fruit_collision.visible = False

    def pac_ghost_collision(self):
        collisions = pygame.sprite.spritecollideany(self.pac_man, self.ghosts)
        if collisions and not self.pac_man.powered_up:
            for ghost in self.ghosts:
                ghost.return_to_center()
            if self.stats.lives > 0:
                self.pac_man.die()
                self.stats.lives -= 1
                self.lives_sprites[self.stats.lives].kill()
                self.death.play()
            else:
                self.stats.new_high_score(self.stats.current_score)
                self.reset_game()
                self.stats.game_status = 0
        elif collisions and self.pac_man.powered_up:
            collisions.return_to_center()
            self.stats.current_score += (2 ^ self.pac_man.ghost_pt_mult) * 100
            self.pac_man.ghost_pt_mult += 1
            self.eatghost.play()

    def pac_portal_collision(self):
        collision = pygame.sprite.spritecollideany(self.pac_man, self.default_ports)
        if self.pac_man.is_teleporting >= 100:
            self.pac_man.is_teleporting = 0
        if collision and self.pac_man.is_teleporting == 0:
            self.pac_man.is_teleporting += 1
            if collision.color == 0:
                self.pac_man.rect.x = self.def_port_list[1].rect.x
            else:
                self.pac_man.rect.x = self.def_port_list[0].rect.x
        elif self.pac_man.is_teleporting != 0:
            self.pac_man.is_teleporting += 1

    def pac_active_portal_collision(self):
        collision = pygame.sprite.spritecollideany(self.pac_man, self.active_ports)
        if self.pac_man.is_teleporting >= 100:
            self.pac_man.is_teleporting = 0
        if collision and self.pac_man.is_teleporting == 0 and self.blue_active and self.orange_active:
            self.pac_man.is_teleporting += 1
            if collision.color == 0:
                self.pac_man.rect.centerx = self.oport.rect.centerx
                self.pac_man.rect.centery = self.oport.rect.centery
            else:
                self.pac_man.rect.centerx = self.bport.rect.centerx
                self.pac_man.rect.centery = self.bport.rect.centery
        elif self.pac_man.is_teleporting != 0:
            self.pac_man.is_teleporting += 1

    def ghost_active_portal_collision(self):
        collision = pygame.sprite.groupcollide(self.ghosts, self.active_ports, False, False)
        if collision:
            for ghost in collision:
                if ghost.is_teleporting == 0 and self.blue_active and self.orange_active:
                    ghost.is_teleporting += 1
                    if collision[ghost][0].color == 0:
                        ghost.rect.centerx = self.oport.rect.centerx
                        ghost.rect.centery = self.oport.rect.centery
                    else:
                        ghost.rect.centerx = self.bport.rect.centerx
                        ghost.rect.centery = self.bport.rect.centery

    def fire_blue_portal(self):
        if not self.blue_active:
            port_loc = self.pac_man.find_portal_spot()
            self.bport = Portal(self.screen, 'blue')
            self.bport.rect.centerx = port_loc[0]
            self.bport.rect.centery = port_loc[1]
            self.active_ports.add(self.bport)
            self.blue_active = True

    def fire_orange_portal(self):
        if not self.orange_active:
            port_loc = self.pac_man.find_portal_spot()
            self.oport = Portal(self.screen, 'orange')
            self.oport.rect.centerx = port_loc[0]
            self.oport.rect.centery = port_loc[1]
            self.active_ports.add(self.oport)
            self.orange_active = True

    # returns x y position for retrieval of object from maze obj 2d array
    # real=true for top left xy, real=false for bot right
    @staticmethod
    def get_obj_pos(obj):
        x = int(obj.rect.x / Maze.BRICK_SIZE)
        y = int(obj.rect.y / Maze.BRICK_SIZE)
        return x, y

    # checks for possible collision, direction is 1 up, 2 right, 3 down, 4 left
    def front_path_is_clear(self, direction, obj):
        obj_pos = self.get_obj_pos(obj)
        if type(obj) is Pacman:
            if direction == 1:
                return self.rows[obj_pos[1]][obj_pos[0] + 1] != 'X' and self.rows[obj_pos[1]][obj_pos[0] + 1] != 'S'
            if direction == 2:
                return self.rows[obj_pos[1] + 1][obj_pos[0] + 3] != 'X' \
                       and self.rows[obj_pos[1] + 1][obj_pos[0] + 3] != 'S'
            if direction == 3:
                return self.rows[obj_pos[1] + 3][obj_pos[0] + 1] != 'X' \
                       and self.rows[obj_pos[1] + 3][obj_pos[0] + 1] != 'S'
            if direction == 4:
                return self.rows[obj_pos[1] + 1][obj_pos[0]] != 'X' and self.rows[obj_pos[1] + 1][obj_pos[0]] != 'S'
        else:
            if direction == 1:
                return self.rows[obj_pos[1]][obj_pos[0] + 1] != 'X'
            if direction == 2:
                return self.rows[obj_pos[1] + 1][obj_pos[0] + 3] != 'X'
            if direction == 3:
                return self.rows[obj_pos[1] + 3][obj_pos[0] + 1] != 'X'
            if direction == 4:
                return self.rows[obj_pos[1] + 1][obj_pos[0]] != 'X'

    def left_is_clear(self, obj):
        flag = True
        for i in range(2, 8):
            if self.screen.get_at((obj.rect.x - 2, obj.rect.y + i)) == (36, 28, 252):
                flag = False
        for i in range(25, 32):
            if self.screen.get_at((obj.rect.x - 2, obj.rect.y + i)) == (36, 28, 252):
                flag = False
        return flag

    def right_is_clear(self, obj):
        flag = True
        for i in range(2, 8):
            if self.screen.get_at((obj.rect.x + 35, obj.rect.y + i)) == (36, 28, 252):
                flag = False
        for i in range(25, 32):
            if self.screen.get_at((obj.rect.x + 35, obj.rect.y + i)) == (36, 28, 252):
                flag = False
        return flag

    def bot_is_clear(self, obj):
        flag = True
        for i in range(2, 8):
            if self.screen.get_at((obj.rect.x + i, obj.rect.y + 35)) == (36, 28, 252):
                flag = False
        for i in range(25, 32):
            if self.screen.get_at((obj.rect.x + i, obj.rect.y + 35)) == (36, 28, 252):
                flag = False
        return flag

    def top_is_clear(self, obj):
        flag = True
        for i in range(2, 8):
            if self.screen.get_at((obj.rect.x + i, obj.rect.y - 3)) == (36, 28, 252):
                flag = False
        for i in range(25, 32):
            if self.screen.get_at((obj.rect.x + i, obj.rect.y - 3)) == (36, 28, 252):
                flag = False
        return flag

    def new_level(self):
        self.maze_obj = []
        self.pac_dots.empty()
        self.power_dots.empty()
        self.active_ports.empty()
        self.bport = None
        self.oport = None
        self.blue_active = False
        self.orange_active = False
        self.default_ports.empty()
        self.def_port_list = []
        for ghost in self.ghosts:
            ghost.return_to_center()
            ghost.scared_timer = 0
            ghost.scared = False
        self.ghosts.empty()
        self.pac_man.power_timer = 0
        self.pac_man.powered_up = False
        self.stats.game_speed += 2
        self.stats.current_level += 1
        self.ambient.stop()
        self.ambient_playing = False
        self.powersound.stop()
        self.power_playing = False
        self.lives_sprites = []
        self.lives_counter.empty()
        self.fruits.empty()
        self.build()
        pygame.time.wait(700)

    def reset_game(self):
        self.maze_obj = []
        self.lives_sprites = []
        self.lives_counter.empty()
        self.pac_dots.empty()
        self.power_dots.empty()
        self.active_ports.empty()
        self.bport = None
        self.oport = None
        self.blue_active = False
        self.orange_active = False
        self.default_ports.empty()
        self.def_port_list = []
        for ghost in self.ghosts:
            ghost.return_to_center()
        self.ghosts.empty()
        self.stats.game_speed = 60
        self.stats.current_level = 0
        self.stats.lives = 3
        self.stats.current_score = 0
        self.radio.stop()
        self.ambient_playing = False
        self.power_playing = False
        self.fruits.empty()
        self.gameover.play()
        self.build()
        self.screen.fill((0, 0, 0))
        pygame.time.wait(700)

    def show_menu(self, anim):
        self.screen.fill((0, 0, 0))
        self.check_menu_events()
        anim.update()
        self.screen.blit(self.title, self.title_rect)
        self.start_button.draw_button()
        self.scores_button.draw_button()
        anim.blitme()

    def create_menu(self):
        self.title = pygame.image.load('images/title.png')
        self.title = pygame.transform.scale(self.title, (750, 750))
        self.title_rect = self.title.get_rect()
        self.title_rect.x = 80
        self.title_rect.y = 100

        self.start_button = Button(self.screen, "PLAY GAME", 1)
        self.scores_button = Button(self.screen, "HIGH SCORES", 2)
        return Animation(self.screen, self)

    def check_menu_events(self):
        m_x, m_y = pygame.mouse.get_pos()
        if self.start_button.rect.collidepoint(m_x, m_y):
            self.start_button.lightup()
        else:
            self.start_button.lightdown()

        if self.scores_button.rect.collidepoint(m_x, m_y):
            self.scores_button.lightup()
        else:
            self.scores_button.lightdown()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if self.start_button.rect.collidepoint(m_x, m_y):
                    self.stats.game_status = 1
                    self.intro.play()
                    time.sleep(3.5)
                elif self.scores_button.rect.collidepoint(m_x, m_y):
                    self.stats.show_score_list()
