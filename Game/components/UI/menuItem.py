# Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015 - Penaz <penazarea@altervista.org>

# from libs import animation
import pygame
import os


class menuitem(object):
    """ Represents a menu item """

    def __init__(self, unselected, selected, location, function, config):
        """
        Default constructor
        :param unselected: The surface representing the unselected button
        :param selected: The surface representing the selected button (hovered)
        :param location: Location of the top-left corner of the menu element
        :param function: Usually a lambda, recalled by the button when used

        :return: Nothing
        """
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
        self.sound.set_volume((config.getfloat("Sound",  "menuvolume"))/100)
        self.confirmSound.set_volume((config.getfloat("Sound",
                                                      "menuvolume"))/100)

    def makeSelected(self):
        """ Turns the element status to "Selected" """
        self.image = self.selected
        self.selectedStatus = True
        self.sound.play()

    def makeUnselected(self):
        """ Turns the element status to "Unselected" """
        self.image = self.unselected
        self.selectedStatus = False

    def update(self):
        """
        Changes the status if the update function is called

        #MIGHT NEED DEPRECATION#
        """
        if self.selected:
            self.makeSelected()
        else:
            self.makeUnselected()
