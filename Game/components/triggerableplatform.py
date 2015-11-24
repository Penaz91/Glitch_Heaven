#!/usr/bin/env python3
import pygame


class TriggerablePlatform(pygame.sprite.Sprite):
    """
    Represents a mobile platform that can be triggered
    inherits properties from MobilePlatform
    """
    def __init__(self, x, y, vertical, spd, *groups, game):
        """
        Default Constructor

        Keyword Arguments:
        - x: The x coord of the top left corner
        - y: The y coord of the top left corner
        - *groups: A collection of sprite groups to add the item to.
        - game: The game istance.

        Returns:
        - Nothing
        """
        super(TriggerablePlatform, self).__init__(*groups)
        self.image = pygame.surface.Surface((100, 32))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vertical = vertical
        if vertical:
            self.xspeed = 0
            self.yspeed = spd
        else:
            self.yspeed = 0
            self.xspeed = spd
        self.direction = 1
        game.plats.add(self)

    def update(self, dt, game):
        """
        Update method

        Keyword Arguments:
        - dt: The unit of time (clock.tick/1000.)
        - game: The game istance

        Returns:
        - Nothing
        """
        self.dt = dt
        self.rect.x += self.direction * self.xspeed * dt    # |
        self.rect.y += self.direction * self.yspeed * dt    # | Moves platform
        # Reverses the platform when a "PlatReverse" trigger is touched
        # v-----------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'PlatReverse'):
            if self.vertical:
                if self.direction > 0:
                    self.rect.bottom = cell.top
                else:
                    self.rect.top = cell.bottom
            else:
                if self.direction > 0:
                    self.rect.right = cell.left
                else:
                    self.rect.left = cell.right
            self.direction *= -1
        # ^------------------------------------------------------------------^
