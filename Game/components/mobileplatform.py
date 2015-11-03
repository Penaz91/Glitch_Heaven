#!/usr/bin/env python3
import pygame


class MobilePlatform(pygame.sprite.Sprite):
    """ A simple object with image and position """

    def __init__(self, x, y, *groups, game, surface):
        """
        Default constructor

        :param x: The horizontal position of the item
        :param y: The vertical position of the item
        :param *groups: A collection of sprite groups to add the item to
        :param game: The game instance
        :param surface: The image that the item should represent

        :return: Nothing
        """
        super(MobilePlatform, self).__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect()
        self.screenx, self.screeny = x, y
        self.rect.x, self.rect.y = game.tilemap.pixel_to_screen(x, y)


    def update(self, dt, game):
        """ Dummy Update Method """
        pass