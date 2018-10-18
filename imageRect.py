import pygame


class Image(pygame.sprite.Sprite):
    def __init__(self, screen, image_name, height, width):
        super(Image, self).__init__()
        self.screen = screen
        name = 'images/' + image_name + '.png'

        img = pygame.image.load(name)
        img = pygame.transform.scale(img, (height, width))
        self.rect = img.get_rect()
        self.rect.left -= self.rect.width/2
        self.rect.top -= self.rect.height/2
        self.image = img
