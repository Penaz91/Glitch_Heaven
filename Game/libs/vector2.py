#!/usr/bin/env python
# --------------------------------------------------
# Vector2
# A simple and Lightweight vector class in 2D
# Part of the Glitch_Heaven Project
# Copyright 2016 Penaz - penazarea@altervista.org
# --------------------------------------------------
from math import sqrt


class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector(x = {0}, y = {1})".format(self.x, self.y)

    def __add__(self, b):
        return Vector(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Vector(self.x - b.x, self.y - b.y)

    def scale(self, scalef):
        self.x *= scalef
        self.y *= scalef

    def get_magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def get_normalized(self):
        mag = self.get_magnitude()
        return Vector(self.x/mag, self.y/mag)

    def normalize(self):
        mag = self.get_magnitude()
        self.x /= mag
        self.y /= mag

    def zero(self):
        self.x = 0
        self.y = 0
