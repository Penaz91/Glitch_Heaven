# Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015 - Penaz <penazarea@altervista.org>

# from libs import animation
import pygame
import os

""" Represents a menu item """
class menuitem(object):
    
    """
    Default constructor
    :param unselected: The surface representing the unselected button
    :param selected: The surface representing the selected button (hovered)
    :param location: Location of the top-left corner of the menu element
    :param function: Usually a lambda, recalled by the button when clicked/used
    
    :return: Nothing
    """
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

    """ Turns the element status to "Selected" """
    def makeSelected(self):
        self.image = self.selected
        self.selectedStatus = True
        self.sound.play()

    """ Turns the element status to "Unselected" """
    def makeUnselected(self):
        self.image = self.unselected
        self.selectedStatus = False

    """ 
    Changes the status if the update function is called
    
    #MIGHT NEED DEPRECATION#
    """
    def update(self):
        if self.selected:
            self.makeSelected()
        else:
            self.makeUnselected()
