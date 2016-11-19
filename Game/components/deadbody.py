# Deadbody Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>

import pygame
from components.mobileplatform import MobilePlatform
from os.path import join as pjoin


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
                    pjoin("resources",
                          "sprites",
                          "player.png")).convert_alpha()
        if game.config["Video"]["permanentbodies"]:
            self.update = self.dummyUpdate
        else:
            self.age = 300.
            self.update = self.realupdate
        MobilePlatform.__init__(self, x, y, *groups, game=game,
                                surface=self.img)

    def dummyUpdate(self, dt, game):
        pass

    def realupdate(self, dt, game):
        self.age -= dt;
        if self.age <=0:
            self.kill()
