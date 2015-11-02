#!/usr/bin/env python3
import pygame
from components.mobileplatform import MobilePlatform
import os

""" Represents a dead player body, for the permbody glitch, inherits properties from mobileplatform """
class DeadBody(MobilePlatform):

    """
    Default Constructor
    
    :param x: The horizontal position of the top-left corner of the sprite
    :param y: The vertical position of the top-left corner of the sprite
    :param *groups: A self-unpacking collection of sprite groups to add the item to
    :param game: The game istance.
    
    :return: Nothing
    """
    def __init__(self, x, y, *groups, game):
        self.img = pygame.image.load(
                    os.path.join("resources",
                                 "sprites",
                                 "player.png")).convert_alpha()
        MobilePlatform.__init__(self, x, y, *groups, game=game,
                                surface=self.img)

    """ Dummy update method """
    def update(self, dt, game):
        pass
