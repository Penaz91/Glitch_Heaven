#!/usr/bin/env python3
import pygame
from components.mobileplatform import MobilePlatform
import os


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

    def update(self, dt, game):
        """
        Update method

        Keyword Arguments:
        - dt: The unit of time (clock.tick/1000.)
        - game: The game istance

        Returns:
        - Nothing
        """
        self.age -= 1
        if self.age == 0:
            self.kill()
            game.setHelpFlag(False)     # Allows the sign to be enabled again
