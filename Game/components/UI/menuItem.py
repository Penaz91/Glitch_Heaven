# Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015 - Penaz <penazarea@altervista.org>

# from libs import animation
import pygame
import os


class menuitem(object):
    
    def __init__(self, unselected, selected, location, function):
        self.unselected = unselected
        self.selected = selected
        self.rect = self.unselected.get_rect()
        self.location = location
        self.rect.x, self.rect.y = location
        self.image = self.unselected
        self.selectedStatus = False
        self.function = function
        self.sound = pygame.mixer.Sound(os.path.join("resources",
                                            "sounds",
                                            "menuSelection.wav"))
        self.confirmSound = pygame.mixer.Sound(os.path.join("resources",
                                                            "sounds",
                                                            "select.wav"))


    def makeSelected(self):
        self.image = self.selected
        self.selectedStatus = True
        self.sound.play()

    def makeUnselected(self):
        self.image = self.unselected
        self.selectedStatus = False

    def update(self):
        if self.selected:
            self.makeSelected()
        else:
            self.makeUnselected()
