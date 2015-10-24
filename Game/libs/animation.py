# Animation/Frame generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os


class Animation(object):
    def __init__(self):
        self.frames = []
        self.currentframe = -1

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()
    # Python2 Compatibility Layer

    def next(self):
        self.currentframe = (self.currentframe+1) % len(self.frames)
        toret = self.frames[self.currentframe]
        return toret

    def loadFromDir(self, directory):
        self.frames = [pygame.image.load(
            os.path.join(directory, f)).convert_alpha()
                       for f in os.listdir(directory)
                       if os.path.isfile(os.path.join(directory, f))]
        #Testing stuff
#        print([(os.path.join(directory, f))
#                       for f in os.listdir(directory)
#                       if os.path.isfile(os.path.join(directory, f))])
