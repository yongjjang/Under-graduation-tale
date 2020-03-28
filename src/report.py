import pygame
import random


class Report(pygame.sprite.Sprite):
    def __init__(self, report_data, font, width, ):
        self.report = report_data
        self.font = font
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface([45, 30])
        self.surface.fill(pygame.Color(0, 0, 0))
        self.x, self.y = random.randint(0, width - 200), 0
        self.speed = 1
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.label = self.font.render(self.report, 30, (255, 255, 255))

    def update(self):

        self.y = self.y + random.randint(1, 4) * self.speed
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
