# TextBox Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame


class textBox(object):
    white = (255, 255, 255)

    def __init__(self, screen, font, message):
        self.buffer = []
        self.screen = screen
        self.font = font
        msg = self.font.render(message, False, self.white)
        self.writings = [
            (msg, msg.get_rect()),
        ]
        msg = (self.font.render("Backspace to delete - Enter to confirm", False, self.white))
        self.writings.append((msg, msg.get_rect()))
        self.surface = pygame.surface.Surface((800, 200), pygame.SRCALPHA)
        self.catching = True
        self._accepted_keys_ = [
            pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e,
            pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j,
            pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o,
            pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
            pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y,
            pygame.K_z, pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
            pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
            pygame.K_9, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3,
            pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8,
            pygame.K_KP9
        ]
        
    def get_input(self):
        self.catching = True
        while self.catching:
            self.surface.fill((74, 74, 74, 5))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.buffer)!=0:
                            self.buffer.pop()
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        self.catching = False
                        return "".join(self.buffer)
                    elif event.key in self._accepted_keys_:
                        if not (pygame.key.get_mods() & pygame.KMOD_LCTRL):
                            self.buffer.append(event.unicode)
            write = self.font.render("".join(self.buffer), False, self.white)
            wrect = write.get_rect()
            wrect.center = self.surface.get_rect().center
            self.surface.blit(write, wrect)
            self.writings[0][1].center = self.surface.get_rect().center
            self.writings[0][1][1] = 10
            self.writings[1][1].center = self.surface.get_rect().center
            self.writings[1][1][1] = 160
            for item in self.writings:
                self.surface.blit(item[0],item[1])
            screen.blit(self.surface, (0, 200))
            pygame.display.update()
            
if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Arial", 24)
    img = pygame.image.load("bg.png").convert_alpha()
    screen.blit(img, (0, 0))
    input = textBox(screen, font, "Insert your savefile name")
    text = input.get_input()
    print(text)