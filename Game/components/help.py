# Help sign component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from os.path import join as pjoin
import pygame
from components.mobileplatform import MobilePlatform
from libs.textAnimation import animatedText


class Help(MobilePlatform):
    """
    Represents a helping Sign/Terminal,
    inherits properties from MobilePlatform
    """
    def __init__(self, centerx, lowy, *groups, game, Text):
        """
        Default Constructor

        Keyword Arguments:
        - centerx: The horizontal center of the text
        - lowy: The low side of the text, relative to position of the player.
        - *groups: A collection of sprite groups to add the item to.
        - game: The game istance.
        - Text: The text that has to be written on the help tip.

        Returns:
        - Nothing
        """
        """self.font = pygame.font.Font(pjoin("resources",
                                           "fonts",
                                           "TranscendsGames.otf"),
                                     24)"""
        self.surfimg = animatedText(Text)
        self.img = self.surfimg.surface
        self.size = self.img.get_rect()
        self.x = centerx - (self.size.width/2)
        self.y = lowy - (self.size.height*game.gravity)
        MobilePlatform.__init__(self, self.x, self.y, *groups, game=game,
                                surface=self.img)
        game.helptxts.add(self)
        self.age = 300

    def update(self, dt, game):
        """
        Update method

        Keyword Arguments:
        - dt: The unit of time (clock.tick/1000.)
        - game: The game istance

        Returns:
        - Nothing
        """
        self.surfimg.update(dt)
        self.age -= 1
        if self.age == 0:
            self.kill()
            game.helpflagActive = False
