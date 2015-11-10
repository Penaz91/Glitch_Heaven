# Animation/Frame generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os


class Animation(object):
    """ This is a simple library that stores frames for a simple animation """

    def __init__(self):
        """ Constructor - No parameters """
        self.frames = []
        self.currentframe = -1      # Setting this at -1 so the first call of next() returns the frame 0

    def __iter__(self):
        """ Allows to return an iterator if necessary """
        return self

    def __next__(self):
        """ Python2 Compatibility Layer"""
        return self.next()

    def next(self):
        """
        This method returns the next frame in the animation,
        in a ring array fashion

        Returns:
        - Next frame from the frame list
        """
        self.currentframe = (self.currentframe+1) % len(self.frames)     # Returns the frame number in a circular fashion, 0 -> ... -> n-1 -> n -> 0
        toret = self.frames[self.currentframe]
        return toret

    def loadFromDir(self, directory):
        """
        Loads the frames from a given directory using List generators,
        frames are sorted by name

        Keyword Arguments:
        - directory: The Directory to load the frames from

        Returns:
        - Nothing
        """
        x = [(os.path.join(directory, f))
             for f in os.listdir(directory)
             if os.path.isfile(os.path.join(directory, f))]
        self.frames = [pygame.image.load(y).convert_alpha() for y in sorted(x)]
