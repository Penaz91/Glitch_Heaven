#!/usr/bin/env python3
# TODO: Add Copyright Info here
import pygame
from player import Player
from libs import tmx
import os
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
        others=pygame.sprite.Group()
        """"p=Player(screen)
        sprites=pygame.sprite.Group()
        sprites.add(p)"""
        # FIXME: Loading the background makes the player disappear
        #bg=pygame.image.load(os.path.join("resources","backgrounds","Back1.png"))
        middle=pygame.image.load("resources/backgrounds/Back2.png").convert_alpha()
        self.tilemap = tmx.load('data/maps/TestMapScroll.tmx',screen.get_size())
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('player')[0]
        self.player = Player((start_cell.px,start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        self.backpos=(0,0)
        self.middlepos=(0,0)
        """Game Loop"""
        while self.running:
            dt=self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
            # TODO: Verify correct implementation of drawing
            screen.fill((0,0,0))
            #screen.blit(bg,self.backpos)
            self.tilemap.update(dt/1000., self)
            screen.blit(middle,self.middlepos)
            self.tilemap.draw(screen)
            pygame.display.flip()
        pygame.quit()
        quit()