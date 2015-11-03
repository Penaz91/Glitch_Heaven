#!/usr/bin/env python3
import pygame
from components.mobileplatform import MobilePlatform
import os

"""
Represents a helping Sign/Terminal,
inherits properties from MobilePlatform
"""


class Help(MobilePlatform):

    """
    Default Constructor

    :param centerx: The horizontal center of the text
    :param lowy: The low side of the text, relative to position of the player.
    :param *groups: A collection of sprite groups to add the item to.
    :param game: The game istance.
    :param Text: The text that has to be written on the help tip.

    :return: Nothing
    """
    def __init__(self, centerx, lowy, *groups, game, Text):
        self.font = pygame.font.Font(os.path.join("resources",
                                                  "fonts",
                                                  "TranscendsGames.otf"),
                                     24)
        self.img = self.font.render(Text, True, (255, 0, 0),
                                    (0, 0, 0))
        self.size = self.img.get_rect()
        self.x = centerx - (self.size.width/2)
        self.y = lowy - (self.size.height*game.gravity)
        MobilePlatform.__init__(self, self.x, self.y, *groups, game=game,
                                surface=self.img)
        game.helptxts.add(self)
        self.age = 300

    """
    Update method

    :param dt: The unit of time (clock.tick/1000.)
    :param game: The game istance

    :return: Nothing
    """
    def update(self, dt, game):
        self.age -= 1
        if self.age == 0:
            self.kill()
            game.setHelpFlag(False)
