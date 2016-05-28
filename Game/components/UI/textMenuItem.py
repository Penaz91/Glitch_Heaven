# Text Menu Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 - Penaz <penazarea@altervista.org>
from components.UI.menuItem import menuitem
from libs.textGlitcher import makeGlitched


class textMenuItem(menuitem):
    white = (255, 255, 255)

    def __init__(self, unselectedtxt, selectedtxt, location,
                 onhover, function, config, sounds, font):
        self.unselimg = font.render(unselectedtxt, False, self.white)
        self.selimg = makeGlitched(selectedtxt, font)
        super().__init__(self.unselimg, self.selimg, location, onhover,
                         function, config, sounds)
