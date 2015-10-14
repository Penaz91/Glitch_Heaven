# Animation/Frame generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penaz@altervista.org>
from os import listdir
from os.path import isfile,join
import pygame
class Animation(object):
    def __init__(self):
        self.frames=[]
        self.currentframe=0
    def __iter__(self):
        return self
    def __next__(self):
        return self.next()
    # Python2 Compatibility Layer
    def next(self):
        toret=self.frames[self.currentframe]
        self.currentframe=(self.currentframe+1)%len(self.frames)
        return toret
    def loadFromDir(self,directory):
        self.frames=[pygame.image.load(join(directory,f)) for f in listdir(directory) if isfile(join(directory,f))]