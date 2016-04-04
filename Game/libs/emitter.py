# Particle Emitter
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 - Penaz <penazarea@altervista.org>
from libs import particle


class Emitter(object):
    """ Represents a particle emitter"""

    def __init__(self, location, sc, ec, xstr, ystr, sg, tm):
        """
        Default constructor

        Keyword Arguments:
        - Location: 2-tuple representing the position of the emitter.
        - xstr: The horizontal strength of the emitter.
        - ystr: The Vertical strength of the emitter.
        - sg: The sprite group to add particles to
        - sc: Starting color
        - ec: Ending color
        """
        self.location = location
        self.xstr = xstr
        self.ystr = ystr
        self.spritegroup = sg
        self.sc = sc
        self.ec = ec
        self.tm = tm

    def emit(self, xst, yst):
        """
        Emits the particles
        """
        particle.Particle(self.location, self.sc, self.ec, self.xstr*xst,
                          self.ystr*yst, self.tm, self.spritegroup)
        particle.Particle(self.location, self.sc, self.ec, xst*2*self.xstr,
                          yst*self.ystr, self.tm, self.spritegroup)
        particle.Particle(self.location, self.sc, self.ec, xst*self.xstr,
                          yst*2*self.ystr, self.tm, self.spritegroup)

    def move(self, newlocation):
        self.location = newlocation
