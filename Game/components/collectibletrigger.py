# CollectibleTrigger component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
#
import pygame
import os
from libs.timedanimation import TimedAnimation as TAni
class CollectibleTrigger(pygame.sprite.Sprite):
    """ A simple object with image and position """

    def __init__(self, x, y, game, *trigger):
        """
        Default constructor

        Keyword Arguments:
        - x: The horizontal position of the item
        - y: The vertical position of the item
        - trigger: The glitches that will be triggered
        - *groups: A collection of sprite groups to add the item to

        Returns:
        - Nothing
        """
        super(CollectibleTrigger, self).__init__()
        self.triggers = trigger[0].split(",")
        self.ani = TAni([1,0.25,0.25,0.25,0.25,0.25,0.25,0.25])
        self.ani.loadFromDir(os.path.join("resources",
                                          "sprites",
                                          "GlitchTrigger"))
        self.image = self.ani.first()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        """
        self.rect = self.image.get_rect()
        self.screenx, self.screeny = x, y
        """
    def update(self, dt, game):
        self.image = self.ani.next(dt)

    def toggle(self, game):
        for glitch in self.triggers:
            game.toggleGlitch(glitch)