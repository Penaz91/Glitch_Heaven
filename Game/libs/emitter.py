# Particle Emitter
# Part of the Glitch_Heaven Project
# Copyright 2015 - Penaz <penazarea@altervista.org>
from libs import particle


class Emitter(object):
    """ Represents a particle emitter"""

    def __init__(self, location, sc, ec, xstr, ystr, sg):
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

    def emit(self):
        """
        Emits the particles
        """
        particle.Particle(self.location, self.sc, self.ec, self.xstr,
                          self.ystr, self.spritegroup)
        particle.Particle(self.location, self.sc, self.ec, 2*self.xstr,
                          self.ystr, self.spritegroup)
        particle.Particle(self.location, self.sc, self.ec, self.xstr,
                          2*self.ystr, self.spritegroup)

    def move(self, newlocation):
        self.location = newlocation

# ----------TESTING AREA----------
"""
pygame.init()
screen = pygame.display.set_mode((640, 480))
group = pygame.sprite.Group()
clock = pygame.time.Clock()
player = pygame.Surface((32, 32))
player.fill((255, 255, 255))
x = 320
y = 240
leftemitter = Emitter((x, y+32), (255, 0, 0), (0, 255, 0), -1, -1, group)
rightemitter = Emitter((x+32, y+32), (255, 0, 0), (0, 255, 0), 1, -1, group)
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 5
                rightemitter.move((x+32, y+32))
                rightemitter.emit()
            if event.key == pygame.K_RIGHT:
                x += 5
                leftemitter.move((x, y+32))
                leftemitter.emit()
    screen.fill((0, 0, 0))
    screen.blit(player, (x, y))
    group.draw(screen)
    group.update()
    pygame.display.flip()
"""
