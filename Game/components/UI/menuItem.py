# Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 - Penaz <penazarea@altervista.org>

# from libs import animation


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
        self.unselected = unselected
        self.selected = selected
        self.rect = self.unselected.get_rect()
        self.location = location
        self.rect.x, self.rect.y = location
        self.image = self.unselected
        self.selectedStatus = False
        self.function = function
        self.onhover = onhover
        self.sound = sounds["menu"]["select"]
        self.confirmSound = sounds["menu"]["confirm"]

    def makeSelected(self):
        """ Turns the element status to "Selected" """
        self.image = self.selected
        self.selectedStatus = True
        self.onhover()
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
