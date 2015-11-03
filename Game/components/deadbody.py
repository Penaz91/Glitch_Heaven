#!/usr/bin/env python3
import pygame
from components.mobileplatform import MobilePlatform
import os


class DeadBody(MobilePlatform):
    """
    Represents a dead player body, for the permbody glitch,
    inherits properties from mobileplatform
    """

    def __init__(self, x, y, *groups, game):
        """
        Default Constructor

        Keyword Arguments:
        - x: The horizontal position of the top-left corner of the sprite
        - y: The vertical position of the top-left corner of the sprite
        - *groups: A collection of sprite groups to add the item to
        - game: The game istance

        Returns:
        - Nothing
        """
        self.img = pygame.image.load(
                    os.path.join("resources",
                                 "sprites",
                                 "player.png")).convert_alpha()
        MobilePlatform.__init__(self, x, y, *groups, game=game,
                                surface=self.img)

    def update(self, dt, game):
        """ Dummy update method """
        pass
