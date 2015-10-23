# Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015 - Penaz <penazarea@altervista.org>

# from libs import animation


class menuitem(object):

    def __init__(self, unselected, selected, location):
        self.unselected = unselected
        self.selected = selected
        self.rect = self.unselected.get_rect()
        self.location = location
        self.rect.x, self.rect.y = location
        self.image = self.unselected
        self.selectedStatus = False

    def makeSelected(self):
        self.image = self.selected
        self.selectedStatus = True

    def makeUnselected(self):
        self.image = self.unselected
        self.selectedStatus = False

    def isSelected(self):
        if self.selected:
            return True
        else:
            return False

    def update(self):
        if self.selected:
            self.makeSelected()
        else:
            self.makeUnselected()
