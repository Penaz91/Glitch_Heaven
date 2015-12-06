# Meter Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org
import pygame


class Meter(object):
    """
    A basic meter for audio settings
    """
    # TODO: Add a way to make the slider really work when you keep the
    #       mouse button pressed
    def __init__(self, location, size, config, what):
        """
        Constructor

        Keyword Arguments:
        - location = A 2-tuple representing the location of the items
        - size = A 2-tuple representing the size of the bar, defaults to 0,0
        """
        self.location = location
        self.size = size
        self.config = config
        self.what = what
        self.image = pygame.surface.Surface(((size[0]), (size[1])),
                                            pygame.SRCALPHA,
                                            32).convert_alpha()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.location
        self.filler = pygame.surface.Surface((0, size[1]),
                                             pygame.SRCALPHA,
                                             32).convert_alpha()
        self.fillerrect = self.filler.get_rect()
        self.filler.fill((255, 0, 0))
        self.draw_from_x(int(self.config.getfloat("Sound", self.what)))

    def set_quantity(self, mousepos):
        """
        Sets the volume quantity according to the position of the mouse

        Keyword Arguments:
        - mousepos = a 2-tuple representing the mouse position
        """
        x = ((mousepos[0] - self.rect.x))
        self.filler = pygame.surface.Surface((x, self.size[1]),
                                             pygame.SRCALPHA,
                                             32).convert_alpha()
        self.fillerrect = self.filler.get_rect()
        self.filler.fill((255, 0, 0))
        self.fillerrect.x, self.fillerrect.y = self.location
        self.config.set("Sound", self.what, str((x/(self.rect.width))*100))
        with open("game.conf", "w") as conf:
            self.config.write(conf)
        return (x/(self.rect.width))*100

    def draw_from_x(self, x):
        """
        Internal overlay resizing routing

        Keyword Arguments:
        - x = The updated volume
        """
        self.filler = pygame.surface.Surface(((x/100)*self.size[0],
                                             self.size[1]), pygame.SRCALPHA,
                                             32).convert_alpha()
        self.fillerrect = self.filler.get_rect()
        self.filler.fill((255, 0, 0))

    def increase(self):
        """
        Increases volume by 1%
        Will be used for keyboard
        """
        x = int(self.config.getfloat("Sound", self.what))  # Volume from config
        x += 1
        if x > 100:
            x = 100
        self.draw_from_x(x)
        return x

    def decrease(self):
        """
        Decreases volume by 1%
        Will be used for keyboard
        """
        x = int(self.config.getfloat("Sound", self.what))  # Volume from config
        x -= 1
        if x < 0:
            x = 0
        self.draw_from_x(x)
        return x

    def draw(self, screen):
        """
        Drawing routine

        Keyword Arguments:
        - screen = The screen to write the object to
        """
        screen.blit(self.image, (self.location[0], self.location[1]))
        screen.blit(self.filler, (self.location[0], self.location[1]))
