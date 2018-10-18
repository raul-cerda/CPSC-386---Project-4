import pygame
from maze import Maze
from gamestats import Gamestats


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((627, 700))
        pygame.display.set_caption('Pac-Man')
        self.Clock = pygame.time.Clock()

    def play(self):
        self.screen.fill((0, 0, 0))
        stats = Gamestats(self.screen)
        maze = Maze(self.screen, 'images/maze2.txt', stats, self.Clock)
        anim = maze.create_menu()
        while True:
            if stats.game_status == 0:
                maze.show_menu(anim)
            if stats.game_status == 1:
                maze.update()
            self.Clock.tick(stats.game_speed)
            pygame.display.flip()


game = Game()
game.play()
