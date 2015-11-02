# Animation/Frame generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os

""" This is a simple library that stores frames for a simple animation """
class Animation(object):

    """ Constructor - No parameters """
    def __init__(self):
        self.frames = []
        self.currentframe = -1      # Setting this at -1 so the first call of next() returns the frame 0

    """ Allows to return an iterator if necessary """
    def __iter__(self):
        return self

    """ Python2 Compatibility Layer"""
    def __next__(self):
        return self.next()

    """
    This method returns the next frame in the animation, in a ring array fashion
    
    :return: Next frame from the frame list
    """
    def next(self):
        self.currentframe = (self.currentframe+1) % len(self.frames)     # Returns the frame number in a circular fashion, 0 -> ... -> n-1 -> n -> 0
        toret = self.frames[self.currentframe]
        return toret

    """Loads the frames from a given directory using List generators, frames are sorted by name
    
    :param directory: The Directory to load the frames from
    
    :return: Nothing
    """
    def loadFromDir(self, directory):
        x = [(os.path.join(directory, f))
             for f in os.listdir(directory)
             if os.path.isfile(os.path.join(directory, f))]
        self.frames = [pygame.image.load(y) for y in sorted(x)]