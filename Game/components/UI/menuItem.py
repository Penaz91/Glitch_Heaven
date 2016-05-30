# Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 - Penaz <penazarea@altervista.org>


class menuitem(object):
    """ Represents a menu item """

    def __init__(self, unselected, selected,
                 location, onhover, function, config, sounds):
        """
        Default constructor
        :param unselected: The surface representing the unselected button
        :param selected: The surface representing the selected button (hovered)
        :param location: Location of the top-left corner of the menu element
        :param function: Usually a lambda, recalled by the button when used

        :return: Nothing
        """
        self.unselectedimg = unselected
        self.selectedimg = selected
        self.rect = self.unselectedimg.get_rect()
        self.rect.x, self.rect.y = location
        self.image = self.unselectedimg
        self.selected = False
        self.function = function
        self.onhover = onhover
        self.sound = sounds["menu"]["select"]
        self.confirmSound = sounds["menu"]["confirm"]

    def makeSelected(self):
        """ Turns the element status to "Selected" """
        self.image = self.selectedimg
        self.selected = True
        self.onhover()
        self.sound.play()

    def makeUnselected(self):
        """ Turns the element status to "Unselected" """
        self.image = self.unselectedimg
        self.selected = False