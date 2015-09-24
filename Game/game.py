#!/usr/bin/env python3
import pygame
from player import Player
class Game(object):
    """ Main method """
    def main(self,ss):
        """Variables"""
        self.screensize=ss
        self.running=True
        self.clock=pygame.time.Clock()
        self.fps=30
        self.playerspeed=100

        """Program"""
        pygame.init()
        screen=pygame.display.set_mode(self.screensize)
        pygame.display.set_caption("Glitch_Heaven")
        p=Player(screen)
        sprites=pygame.sprite.Group()
        sprites.add(p)

        """Game Loop"""
        while self.running:
            dt=self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                        p.x_speed=0
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        p.x_speed=self.playerspeed
                    elif event.key==pygame.K_LEFT:
                        p.x_speed=-self.playerspeed
            screen.fill((0,0,0))
            sprites.update(dt)
            pygame.display.flip()
        pygame.quit()
        quit()
