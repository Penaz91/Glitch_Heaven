#!/usr/bin/env python3
# TODO: Add Copyright Info here
import pygame
from player import Player
from libs import tmx
class Game(object):
    """ Main method """
    def main(self,ss):
        """Variables"""
        self.screensize=ss
        self.running=True
        self.clock=pygame.time.Clock()
        self.fps=30

        """Program"""
        pygame.init()
        screen=pygame.display.set_mode(self.screensize)
        pygame.display.set_caption("Glitch_Heaven")
        """"p=Player(screen)
        sprites=pygame.sprite.Group()
        sprites.add(p)"""
        # TODO: Verify Successful loading of the map
        self.tilemap = tmx.load('data/maps/TestMap.tmx',screen.get_size())
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('player')[0]
        self.player = Player((start_cell.px,start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        """Game Loop"""
        while self.running:
            dt=self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
            # TODO: Verify correct implementation of drawing
            self.tilemap.update(dt/1000., self)
            screen.fill((0,0,0))
            self.tilemap.draw(screen)
            pygame.display.flip()
        pygame.quit()
        quit()