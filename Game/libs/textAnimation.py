import pygame
from math import ceil
from os.path import join as pj


class animatedText:

    def __init__(self, text):
        self.x, self.y = 0, 0
        self.text = text
        self.renderedText = ""
        self.index = -1
        self.frametime = 0.02
        self.currtime = 0
        self.font = pygame.font.Font(pj("resources", "fonts", "TranscendsGames.otf"), 18)
        self.fontsurface = self.font.render("", False, (255, 255, 255))
        self.bgsize = [0, 32]
        fsize = (self.font.size(self.text + "_")[0])
        self.hoffset = 0        # For autocentering
        temp = ceil((fsize + 20) / 32)
        self.bgsurface = self.bgGen(temp)
        self.surface = pygame.surface.Surface((self.bgsurface.get_width(), self.bgsurface.get_height()), pygame.SRCALPHA)
        #self.sound = pygame.mixer.Sound("blip.wav")
    
    def bgGen(self, size):
        graphics = pygame.image.load(pj("resources", "tiles", "TextTile.png")).convert_alpha()
        lcorner = (0, 0, 32, 32)
        center = (32, 0, 32, 32)
        rcorner = (64, 0, 32, 32)
        plat = pygame.surface.Surface((32*size, 32), pygame.SRCALPHA)
        if size == 1:
            size = 2
        centrals = size - 2
        plat.blit(graphics, (0, 0), lcorner)
        for i in range(1, centrals+1):
            #i += 1
            plat.blit(graphics, (32*i, 0), center)
        plat.blit(graphics, (32*(size-1), 0), rcorner)
        return plat

    def update(self, dt):
        self.currtime += dt
        if self.currtime >= self.frametime:
            if self.index < len(self.text):
                self.currtime = 0
                self.renderedText = "".join(list(self.text[0:self.index+1]))
                self.renderedText += "_"
                self.index+=1
                #channel = pygame.mixer.find_channel()
                #channel.queue(self.sound)
                #self.sound.play()
                self.hoffset = (self.bgsurface.get_width() - self.font.size(self.renderedText)[0])/2
            else:
                # TODO: Needs optimization (Useless assignments)
                self.frametime = 0.2
                self.currtime = 0
                if "_" in self.renderedText:
                    self.renderedText = self.renderedText[0:len(self.renderedText)-1]
                else:
                    self.renderedText += "_"
        self.fontsurface = self.font.render(self.renderedText, False, (255, 255, 255))
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.bgsurface, (0, 0))
        self.surface.blit(self.fontsurface, (self.hoffset, 7))
            
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.set_num_channels(64)
    screen = pygame.display.set_mode((640, 480))
    txt = animatedText("This is gonna be great /o/")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 0, 0), (20, 70), (600, 70), 3)
        dt = clock.tick(60) / 1000.
        txt.update(dt)
        screen.blit(txt.surface, (50, 50))
        pygame.display.update()