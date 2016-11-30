# CollectibleTrigger component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
#
import pygame
from libs.timedspritesheetanimation import TimedSpritesheetAnimation as TAni


class CollectibleTrigger(pygame.sprite.Sprite):
    """ A simple object with image and position """

    def __init__(self, x, y, game, *trigger, preloaded_animation, message=""):
        """
        Default constructor

        Keyword Arguments:
        - x: The horizontal position of the item
        - y: The vertical position of the item
        - game: The game instance
        - trigger: The glitches that will be triggered

        Returns:
        - Nothing
        """
        super(CollectibleTrigger, self).__init__()
        self.triggers = trigger[0].split(",")
        self.ani = TAni([(1, 1), (0.25, 7)], preloaded_animation)
        self.image = self.ani.next(0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.message = message

    def update(self, dt, game):
        self.image = self.ani.next(dt)

    def toggle(self, game):
        for glitch in self.triggers:
            game.toggleGlitch(glitch, True)
