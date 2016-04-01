# Timed Animation/Frame Generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from libs.animation import Animation
import random


class TimedAnimation(Animation):
    def __init__(self, frametimings):
        super(Animation, self).__init__()
        self.frames = []
        self.currentframe = -1
        self.timings = frametimings
        self.currenttime = 0

    """ Next() remaps itself at runtime to save on comparisons"""
    def next(self, dt):
        self.next = self.next_post
        return self.first()

    def next_post(self, dt):
        self.currenttime += dt
        if self.currenttime >= self.timings[self.currentframe]:
            self.currentframe = (self.currentframe+1) % len(self.frames)
            self.currenttime = 0
        return self.frames[self.currentframe]

    """ Like Next(), rand_next() remaps itself at runtime
    to save on comparisons """
    def rand_next(self, dt):
        self.frame = self.first()
        self.rand_next = self.rand_next_post
        return self.frame

    def rand_next_post(self, dt):
        """
        This method returns the next frame in the animation,
        in a ring array fashion if the timing is passed

        Returns:
        - Next frame from the frame list
        """
        self.currenttime += dt
        if self.currenttime >= self.timings[self.currentframe]:
            self.currenttime = 0
            self.frame = random.choice(self.frames)
        return self.frame

    def first(self):
        self.currentframe = 0
        return self.frames[0]
