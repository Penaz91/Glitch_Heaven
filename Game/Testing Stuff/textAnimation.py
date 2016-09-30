import pygame

class animatedText:

    def __init__(self):
        self.x, self.y = 0, 0
        self.text = "Test Text Here"
        self.renderedText = ""
        self.index = -1
        self.frametime = 0.05
        self.currtime = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.surface = self.font.render("", False, (255, 255, 255))
        self.sound = pygame.mixer.Sound("blip.wav")
        
    def update(self, dt):
        self.currtime += dt
        if self.currtime >= self.frametime:
            if self.index < len(self.text):
                self.currtime = 0
                self.renderedText = "".join(list(self.text[0:self.index+1]))
                self.renderedText += "_"
                self.index+=1
                channel = pygame.mixer.find_channel()
                channel.queue(self.sound)
                self.sound.play()
            else:
                self.currtime = 0
                if "_" in self.renderedText:
                    self.renderedText = self.renderedText[0:len(self.renderedText)-1]
                else:
                    self.renderedText += "_"
        self.surface = self.font.render(self.renderedText, False, (255, 255, 255))
            
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.set_num_channels(64)
    screen = pygame.display.set_mode((640, 480))
    txt = animatedText()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0, 0, 0))
        dt = clock.tick(60) / 1000.
        txt.update(dt)
        screen.blit(txt.surface, (50, 50))
        pygame.display.update()