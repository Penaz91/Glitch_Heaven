# Timed Animation/Frame Generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
from libs.animation import Animation


class TimedAnimation(Animation):
    def __init__(self, frametimings):
        super(Animation, self).__init__()
        self.frames = []
        self.currentframe = -1
        self.timings = frametimings
        self.currenttime = 0
    
    def next(self, dt):
        """
        This method returns the next frame in the animation,
        in a ring array fashion if the timing is passed

        Returns:
        - Next frame from the frame list
        """
        self.currenttime += dt
        if self.currentframe == -1:
            return self.first()
        if self.currenttime >= self.timings[self.currentframe]:
            self.currentframe = (self.currentframe+1) % len(self.frames)     # Returns the frame number in a circular fashion, 0 -> ... -> n-1 -> n -> 0
            self.currenttime = 0
        toret = self.frames[self.currentframe]
        return toret
        
    def first(self):
        self.currentframe = 0
        return self.frames[0]