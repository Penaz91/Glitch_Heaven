# Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015 - Penaz <penazarea@altervista.org>
from libs import animation


class menuitem(object):

    def __init__(self, unselected, selected, rect):
        self.unselected = unselected
        self.selected = selected
        self.rect = rect
        self.makeUnselected()
        self.selected = False

    def makeSelected(self):
        if isinstance(self.selected, animation):
            self.image = self.selected.next()
        else:
            self.image = self.selected
        self.selected = True

    def makeUnselected(self):
        if isinstance(self.unselected, animation):
            self.image = self.unselected.next()
        else:
            self.image = self.unselected
        self.selected = False

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
