import pygame.font
import time


class Gamestats:
    def __init__(self, screen):
        self.screen = screen
        self.current_score = 0
        self.current_level = 0
        self.lives = 3
        self.high_score = 10000
        self.game_speed = 60
        self.game_status = 0

        score_file = open('scores.txt', 'r')
        self.high_scores = score_file.readlines()
        self.high_score = int(self.high_scores[0])
        score_file.close()

        self.font = pygame.font.SysFont('malgunggothic', 30)
        self.score_img = None
        self.score_rect = None
        self.hi_score_img = None
        self.hi_score_rect = None
        self.score_num_img = None
        self.score_num_rect = None
        self.hi_score_num_img = None
        self.hi_score_num_rect = None
        self.prep_hud()

    def reset_stats(self):
        self.update_high_score()
        self.current_score = 0
        self.current_level = 0
        self.lives = 3

    def update_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score

    def prep_hud(self):

        self.score_img = self.font.render('SCORE', True, (255, 255, 255))
        self.score_rect = self.score_img.get_rect()
        self.score_rect.centerx = self.screen.get_rect().right / 5
        self.score_rect.y = 10

        self.hi_score_img = self.font.render('HIGH SCORE', True, (255, 255, 255))
        self.hi_score_rect = self.hi_score_img.get_rect()
        self.hi_score_rect.x = self.screen.get_rect().right / 2
        self.hi_score_rect.y = 10

    def prep_scores(self):
        self.score_num_img = self.font.render(str(self.current_score), True, (255, 255, 255))
        self.score_num_rect = self.score_num_img.get_rect()
        self.score_num_rect.centerx = self.score_rect.centerx
        self.score_num_rect.y = 30

        self.hi_score_num_img = self.font.render(str(self.high_score), True, (255, 255, 255))
        self.hi_score_num_rect = self.hi_score_num_img.get_rect()
        self.hi_score_num_rect.x = self.hi_score_rect.centerx
        self.hi_score_num_rect.y = 30

        self.update_high_score()

    def blitme(self):
        self.prep_scores()
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.hi_score_img, self.hi_score_rect)
        self.screen.blit(self.score_num_img, self.score_num_rect)
        self.screen.blit(self.hi_score_num_img, self.hi_score_num_rect)

    def show_score_list(self):
        lb_image = self.font.render("HIGH SCORES", True, (0, 255, 0))
        lb_rect = lb_image.get_rect()
        lb_rect.centerx = self.screen.get_rect().centerx
        lb_rect.centery = self.screen.get_rect().centery - 100

        score1 = str(int(self.high_scores[0]))
        score1 = self.font.render(score1, True, (255, 255, 255))
        score1_rect = score1.get_rect()
        score1_rect.centerx = self.screen.get_rect().centerx
        score1_rect.centery = self.screen.get_rect().centery - 50

        score2 = str(int(self.high_scores[1]))
        score2 = self.font.render(score2, True, (255, 255, 255))
        score2_rect = score2.get_rect()
        score2_rect.centerx = self.screen.get_rect().centerx
        score2_rect.centery = self.screen.get_rect().centery

        score3 = str(int(self.high_scores[2]))
        score3 = self.font.render(score3, True, (255, 255, 255))
        score3_rect = score3.get_rect()
        score3_rect.centerx = self.screen.get_rect().centerx
        score3_rect.centery = self.screen.get_rect().centery + 50

        self.screen.fill((0, 0, 0))
        self.screen.blit(lb_image, lb_rect)
        self.screen.blit(score1, score1_rect)
        self.screen.blit(score2, score2_rect)
        self.screen.blit(score3, score3_rect)
        pygame.display.flip()
        time.sleep(3.0)
        self.screen.fill((0, 0, 0))

    def new_high_score(self, new_score):
        if new_score > int(self.high_scores[0]):
            self.high_scores[0] = str(new_score)+'\n'
        elif new_score > int(self.high_scores[1]):
            self.high_scores[1] = str(new_score)+'\n'
        elif new_score > int(self.high_scores[2]):
            self.high_scores[2] = str(new_score)+'\n'
        self.save_high_scores()

    # saves the 3 top scores to text file for next game session
    def save_high_scores(self):
        score_file = open('scores.txt', 'w')
        for i in self.high_scores:
            score_file.write(i)
        score_file.close()
