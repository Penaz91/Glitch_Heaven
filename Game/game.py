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
        self.playerspeed=100

        """Program"""
        pygame.init()
        screen=pygame.display.set_mode(self.screensize)
        pygame.display.set_caption("Glitch_Heaven")
        """"p=Player(screen)
        sprites=pygame.sprite.Group()
        sprites.add(p)"""
        # TODO: Verify Successful loading of the map
        """Traceback (most recent call last):
  File "C:\Users\Penaz\Desktop\Progetti\Glitch_Heaven\Game\game.py", line 24, in main
    self.tilemap = tmx.load('data/maps/TestMap.tmx',screen.get_size())
  File "C:\Users\Penaz\Desktop\Progetti\Glitch_Heaven\Game\libs\tmx.py", line 835, in load
    return TileMap.load(filename, viewport)
  File "C:\Users\Penaz\Desktop\Progetti\Glitch_Heaven\Game\libs\tmx.py", line 711, in load
    tilemap.tilesets.add(Tileset.fromxml(tag))
  File "C:\Users\Penaz\Desktop\Progetti\Glitch_Heaven\Game\libs\tmx.py", line 80, in fromxml
    tileset.add_image(c.attrib['source'])
  File "C:\Users\Penaz\Desktop\Progetti\Glitch_Heaven\Game\libs\tmx.py", line 87, in add_image
    image = pygame.image.load(file).convert_alpha()
pygame.error: Couldn't open ../../resources/tiles/WallsTemp.png"""
        self.tilemap = tmx.load('data/maps/TestMap.tmx',screen.get_size())
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('player')['Entrance']
        self.player = Player((start_cell.px,start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
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
            # TODO: Verify correct implementation of drawing
            self.tilemap.update(dt/1000., self)
            screen.fill((0,0,0))
            self.tilemap.draw(screen)
            pygame.display.flip()
        pygame.quit()
        quit()
