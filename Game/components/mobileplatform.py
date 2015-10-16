#!/usr/bin/env python3
import pygame


class MobilePlatform(pygame.sprite.Sprite):
    size = (32, 32)
    playerspeed = 300

    def __init__(self, x, y, *groups, game, surface):
        super(MobilePlatform, self).__init__(*groups)
        #self.image = pygame.image.load(os.path.join("resources",
                                                    #"sprites",
                                                    #"player.png"))
        self.image=surface
        self.rect = self.image.get_rect()
        self.screenx, self.screeny = x, y
        self.rect.x, self.rect.y = game.tilemap.pixel_to_screen(x, y)

    def update(self, dt, game):
        pass
