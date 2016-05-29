# Keyboard Item Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.keyboarditem import KeyboardItem
from libs.textglitcher import makeGlitched


class textKeyboardItem(KeyboardItem):
    white = (255, 255, 255)

    def __init__(self, text, location, onhover,
                 function, config, sounds, log, font):
        self.unselimg = font.render(text, False, self.white).convert_alpha()
        self.selimg = makeGlitched(text, font)
        super().__init__(self.unselimg, self.selimg,
                         location, onhover, function, config, sounds, log)
