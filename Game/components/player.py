# Player component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
#
# ------------------------------------------------
# TODO AREA
# - Reduce boilerplate concerning Common operations with left
#   and right movement.
# - Reduce boilerplate concerning the emission of particles
# - Tie player size to the size of the sprite
# - Find a reason for the code at row 262
# - Tie bouncing mechanics directly to direction via formula,
#   instead of using conditionals, to save CPU power.
# - Separate and compact animation routines
# ------------------------------------------------
import pygame
import os
from components.deadbody import DeadBody
from components.help import Help
from libs import timedanimation
from libs import emitter
import logging
from logging import handlers as loghandler
mod_logger = logging.getLogger("Glitch_Heaven.PlayerEntity")
fh = loghandler.TimedRotatingFileHandler(os.path.join("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
mod_logger.addHandler(fh)
mod_logger.addHandler(ch)


class Player(pygame.sprite.Sprite):
    """ Class representing the player """
    size = (32, 32)     # Might be removed in future+taken from img
    playermaxspeed = 200
    runmultiplier = 2
    playeraccel = 50

    def __init__(self, location, *groups, keys, game):
        """
        Default Constructor

        Keyword Arguments:
        - location: 2-tuple (x,y) representing the location of the player
        - *groups: Collection of sprite groups to add the item to
        - keys: reference to the control keys for movement/actions

        Returns:
        - Nothing
        """
        super(Player, self).__init__(*groups)
        self.glitched = False
        self.jumpsound = pygame.mixer.Sound(os.path.join("resources",
                                                         "sounds",
                                                         "jump.wav"))
        self.jumpsound.set_volume((game.config.getfloat("Sound",
                                                        "sfxvolume"))/100)
        self.deathsound = pygame.mixer.Sound(os.path.join("resources",
                                                          "sounds",
                                                          "death.wav"))
        self.deathsound.set_volume((game.config.getfloat("Sound",
                                                         "sfxvolume"))/100)
        self.bouncesound = pygame.mixer.Sound(os.path.join("resources",
                                                           "sounds",
                                                           "bounce.wav"))
        self.bouncesound.set_volume((game.config.getfloat("Sound",
                                                          "sfxvolume"))/100)
        self.idleani = timedanimation.TimedAnimation([0.25, 0.25, 0.25,
                                                      0.25, 0.25])
        self.idleani.loadFromDir(os.path.join("resources",
                                              "sprites",
                                              "Player",
                                              "Idle"))
        self.gidleani = timedanimation.TimedAnimation([0.25, 0.25, 0.25,
                                                      0.25, 0.25])
        self.gidleani.loadFromDir(os.path.join("resources",
                                               "sprites",
                                               "Glitched_Player",
                                               "Idle"))

        self.image = self.idleani.first()
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.resting = False
        self.y_speed = 0
        self.x_speed = 0
        self.jump_speed = -500
        self.fallingsprite = pygame.image.load(
                os.path.join("resources",
                             "sprites",
                             "Player",
                             "jump_fall.png")).convert_alpha()
        self.jumpsprite = pygame.image.load(
                os.path.join("resources",
                             "sprites",
                             "Player",
                             "jump_rise.png")).convert_alpha()
        self.gfallingsprite = pygame.image.load(
                os.path.join("resources",
                             "sprites",
                             "Glitched_Player",
                             "jump_fall.png")).convert_alpha()
        self.gjumpsprite = pygame.image.load(
                os.path.join("resources",
                             "sprites",
                             "Glitched_Player",
                             "jump_rise.png")).convert_alpha()
        self.direction = 1      # 1=Right, -1=Left
        self.bounced = False    # Used to ignore input when bounced
        self.keys = keys
        self.walkanimation = timedanimation.TimedAnimation([0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06])
        self.walkanimation.loadFromDir(os.path.join("resources",
                                                    "sprites",
                                                    "Player",
                                                    "Walking"))
        self.runanimation = timedanimation.TimedAnimation([0.04, 0.04, 0.04,
                                                           0.04, 0.04, 0.04,
                                                           0.04, 0.04])
        self.runanimation.loadFromDir(os.path.join("resources",
                                                   "sprites",
                                                   "Player",
                                                   "Running"))
        self.gwalkanimation = timedanimation.TimedAnimation([0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06])
        self.gwalkanimation.loadFromDir(os.path.join("resources",
                                                     "sprites",
                                                     "Glitched_Player",
                                                     "Walking"))
        self.grunanimation = timedanimation.TimedAnimation([0.04, 0.04, 0.04,
                                                           0.04, 0.04, 0.04,
                                                           0.04, 0.04])
        self.grunanimation.loadFromDir(os.path.join("resources",
                                                    "sprites",
                                                    "Glitched_Player",
                                                    "Running"))
        self.particles = pygame.sprite.Group()
        self.game = game
        self.running = False
        if game.config.getboolean("Video", "playerparticles"):
            self.leftemitter = emitter.Emitter(self.rect.bottomleft,
                                               (0, 81, 138),
                                               (141, 200, 241), -1, -1,
                                               self.particles)
            self.rightemitter = emitter.Emitter(self.rect.bottomright,
                                                (0, 81, 138),
                                                (141, 200, 241), 1, -1,
                                                self.particles)

    def respawn(self, game):
        """
        Method used to respawn the player after death

        Keyword Arguments:
        - game: The game instance

        Returns:
        - Nothing
        """
        # TODO: Avoid a bug that adds an instance of player to every
        #       respawn
        # If the permbody glitch is active, will add a body at death position
        # v-----------------------------------------------------v
        x, y = game.tilemap.pixel_from_screen(self.rect.x,
                                              self.rect.y)
        mod_logger.info("Player respawned, position of death: (" + str(x) + "," + str(y) + ")")
        if game.glitches["permbodies"]:
            body = DeadBody(x, y, game.sprites, game=game)
            game.deadbodies.add(body)
        if game.glitches["invertedgravity"]:
            game.gravity = -1
        else:
            game.gravity = 1
        self.deathsound.play()
        # ^-----------------------------------------------------^
        # self.kill()     # Kills the player sprite
        # Does a complete respawn of the player
        # v-----------------------------------------------------v
        start_cell = game.tilemap.layers['Triggers'].find('playerEntrance')[0]
        # game.player = Player((start_cell.px, start_cell.py),
        #                     game.sprites, keys=self.keys, game=self.game)
        game.player.rect.x, game.player.rect.y = start_cell.px, start_cell.py
        game.player.y_speed = 0
        game.player.x_speed = 0
        # ^-----------------------------------------------------^

    def animate(self, yspeed, xspeed, resting,
                direction, dt, gravity, running, glitched):
        if glitched:
            if resting:
                # Player is on the ground
                if direction == 1:
                    # Player is pointing right
                    if xspeed == 0:
                        # Player is idle, pointing right
                        self.image = self.gidleani.next(dt)
                    else:
                        # Player is moving right
                        if running:
                            # Player is running rightwards
                            self.image = self.grunanimation.next(dt)
                        else:
                            # Player is walking rightwards
                            self.image = self.gwalkanimation.next(dt)
                elif direction == -1:
                    # Player is pointing left
                    if xspeed == 0:
                        # Player is idle, pointing left
                        self.image = pygame.transform.flip(
                                    self.gidleani.next(dt),
                                    True,
                                    False)
                    else:
                        # Player is moving left
                        if running:
                            # Player is running leftwards
                            self.image = pygame.transform.flip(
                                         self.grunanimation.next(dt),
                                         True,
                                         False)
                        else:
                            # Player is walking leftwards
                            self.image = pygame.transform.flip(
                                         self.gwalkanimation.next(dt),
                                         True,
                                         False)
            else:
                # Player is either jumping or falling
                if direction == 1:
                    # Player is pointing right
                    if yspeed * gravity > 0:
                        # Player is falling
                        self.image = self.gfallingsprite
                    elif yspeed * gravity < 0:
                        # Player is jumping
                        self.image = self.gjumpsprite
                elif direction == -1:
                    # Player is pointing left
                    if yspeed * gravity > 0:
                        # Player is falling
                        self.image = pygame.transform.flip(
                                     self.gfallingsprite,
                                     True,
                                     False)
                    elif yspeed * gravity < 0:
                        # Player is jumping
                        self.image = pygame.transform.flip(
                                     self.gjumpsprite,
                                     True,
                                     False)
        else:
            if resting:
                # Player is on the ground
                if direction == 1:
                    # Player is pointing right
                    if xspeed == 0:
                        # Player is idle, pointing right
                        self.image = self.idleani.next(dt)
                    else:
                        # Player is moving right
                        if running:
                            # Player is running rightwards
                            self.image = self.runanimation.next(dt)
                        else:
                            # Player is walking rightwards
                            self.image = self.walkanimation.next(dt)
                elif direction == -1:
                    # Player is pointing left
                    if xspeed == 0:
                        # Player is idle, pointing left
                        self.image = pygame.transform.flip(
                                    self.idleani.next(dt),
                                    True,
                                    False)
                    else:
                        # Player is moving left
                        if running:
                            # Player is running leftwards
                            self.image = pygame.transform.flip(
                                         self.runanimation.next(dt),
                                         True,
                                         False)
                        else:
                            # Player is walking leftwards
                            self.image = pygame.transform.flip(
                                         self.walkanimation.next(dt),
                                         True,
                                         False)
            else:
                # Player is either jumping or falling
                if direction == 1:
                    # Player is pointing right
                    if yspeed * gravity > 0:
                        # Player is falling
                        self.image = self.fallingsprite
                    elif yspeed * gravity < 0:
                        # Player is jumping
                        self.image = self.jumpsprite
                elif direction == -1:
                    # Player is pointing left
                    if yspeed * gravity > 0:
                        # Player is falling
                        self.image = pygame.transform.flip(
                                     self.fallingsprite,
                                     True,
                                     False)
                    elif yspeed * gravity < 0:
                        # Player is jumping
                        self.image = pygame.transform.flip(
                                     self.jumpsprite,
                                     True,
                                     False)
        if gravity == -1:
            oldimg = self.image
            self.image = pygame.transform.flip(
                         oldimg, False, True)

    def update(self, dt, game):
        """
        Updates the status of the player

        Keyword Arguments:
        - dt: The time slice (clock.tick())
        - game: The Game instance.

        Returns:
        - Nothing
        """
        last = self.rect.copy()     # Copy last position for collision compare
        key = pygame.key.get_pressed()
        if key[self.keys["left"]]:
            self.direction = -1     # Mainly for different bounce mechanics
            if not self.bounced:        # Not bounced away -> control in air
                # Why do i have different control in air if i'm running?
                # This might lead to a change of speed in air
                # Do i want this?
                # v--------------------------------------------------------v
                if key[self.keys["run"]]:
                    self.running = True
                    self.x_speed = max(-self.playermaxspeed * dt *
                                       self.runmultiplier,
                                       self.x_speed-self.playeraccel*dt *
                                       self.runmultiplier)  # Use running speed
                # ^--------------------------------------------------------^
                    # Emits particles if the player is on a surface
                    # Strength is increased because of running
                    # TODO: Tie particles to tilemap, to avoid graphic glitches
                    # v----------------------------------------------------v
                    if self.resting and \
                            game.config.getboolean("Video", "playerparticles"):
                        self.rightemitter.move(self.rect.bottomright)
                        self.rightemitter.emit(2)
                    # ^----------------------------------------------------^
                else:
                    self.running = False
                    self.x_speed = max(-self.playermaxspeed * dt,
                                       self.x_speed -
                                       self.playeraccel*dt)  # Use walk speed
                    # Emits particles if the player is on a surface
                    # TODO: Tie particles to tilemap, to avoid graphic glitches
                    # v----------------------------------------------------v
                    if self.resting and \
                            game.config.getboolean("Video", "playerparticles"):
                        self.rightemitter.move(self.rect.bottomright)
                        self.rightemitter.emit(1)
                    # ^----------------------------------------------------^

        elif key[self.keys["right"]]:
            if not self.bounced:
                self.direction = 1  # Used mainly for bouncy mechanics
                if key[self.keys["run"]]:
                    self.running = True
                    self.x_speed = min(self.playermaxspeed * dt *
                                       self.runmultiplier,
                                       self.x_speed+self.playeraccel * dt *
                                       self.runmultiplier)  # Use run speed
                    # Emits particles if the player is on a surface
                    # Strength is increased because of running
                    # TODO: Tie particles to tilemap, to avoid graphic glitches
                    # v----------------------------------------------------v
                    if self.resting and \
                            game.config.getboolean("Video", "playerparticles"):
                        self.leftemitter.move(self.rect.bottomleft)
                        self.leftemitter.emit(2)
                    # ^----------------------------------------------------^
                else:
                    self.running = False
                    self.x_speed = min(self.playermaxspeed*dt,
                                       self.x_speed +
                                       self.playeraccel*dt)  # Walk Speed
                    # Emits particles if the player is on a surface
                    # Strength is increased because of running
                    # TODO: Tie particles to tilemap, to avoid graphic glitches
                    # v----------------------------------------------------v
                    if self.resting and \
                            game.config.getboolean("Video", "playerparticles"):
                        self.leftemitter.move(self.rect.bottomleft)
                        self.leftemitter.emit(1)
                    # ^----------------------------------------------------^
        else:
            # Gives the player some control over the fall if they're not
            # bounced away from a spring
            # TODO: Find some better way to let player keep control
            # TODO: Tie direction and movement in a formula instead of conds
            # v--------------------------------------------------------------v
            if not self.bounced:
                if self.direction == 1:
                    self.x_speed = max(0, self.x_speed-(self.playeraccel*dt))
                elif self.direction == -1:
                    self.x_speed = min(0, self.x_speed+(self.playeraccel*dt))
            # ^--------------------------------------------------------------^
        self.rect.x += self.x_speed         # Move the player
        if game.glitches["multijump"]:
            if key[self.keys["jump"]]:
                if self.y_speed*game.gravity >= 0:
                    self.jumpsound.play()
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    # If the high jump glitch is active, jumps twice as high
                    # This happens while the multijump glitch is active
                    # v------------------------------------------------------v
                    # TODO ?: tie highjump glitch to jump_speed so i can make
                    #         1 comparison per level loaded
                    if self.y_speed*game.gravity > -(self.jump_speed/2) or\
                            self.resting:
                        if game.glitches["highjump"]:
                            self.y_speed = self.jump_speed*2*game.gravity
                        else:
                            self.y_speed = self.jump_speed*game.gravity
                    # ^------------------------------------------------------^
        elif game.glitches["hover"]:
            if key[self.keys["jump"]]:
                if self.y_speed == 0:
                    self.jumpsound.play()
                self.y_speed = self.jump_speed*game.gravity*0.8
        else:
            if key[self.keys["jump"]] and self.resting:
                self.jumpsound.play()
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    # If the high jump glitch is active, jumps twice as high
                    # v------------------------------------------------------v
                    if game.glitches["highjump"]:
                        self.y_speed = self.jump_speed*2*game.gravity
                    else:
                        self.y_speed = self.jump_speed*game.gravity
                    # ^------------------------------------------------------^
                    self.resting = False    # I jumped, so i'm not on a surface
        if game.glitches["featherfalling"]:
            if game.glitches["ledgejump"]:
                if game.gravity == 1:
                    self.y_speed = (min(200, self.y_speed+20))
                elif game.gravity == -1:
                    self.y_speed = max(-200, self.y_speed-20)
            else:
                if game.gravity == 1:
                    self.y_speed = (min(200, self.y_speed+20))
                elif game.gravity == -1:
                    self.y_speed = max(-200, self.y_speed-20)
        else:
            if game.glitches["ledgejump"]:
                if game.gravity == 1:
                    self.y_speed = (min(400, self.y_speed+40))
                elif game.gravity == -1:
                    self.y_speed = max(-400, self.y_speed-40)
            else:
                if game.gravity == 1:
                    self.y_speed = (min(400, self.y_speed+40))
                elif game.gravity == -1:
                    self.y_speed = max(-400, self.y_speed-40)
        if game.glitches['ledgewalk']:
            if not self.resting:
                self.rect.y += self.y_speed * dt   # Move the player vertically
        else:
            self.rect.y += self.y_speed * dt    # Move the player vertically
        # This avoids the ability to jump in air after leaving a platform
        # TODO: Framework for a "airjump" glitch?
        # v--------------v
        if not game.glitches["ledgejump"] and not game.glitches["ledgewalk"]:
            self.resting = False
        # ^--------------^
        # Moving plats collision check
        # NOTE: This has to stay here to avoid being able to go through
        #       walls while on a platform
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.plats, False)
        for block in collision:
            if block.active:
                # ENHANCEMENT: Change the collision detection with a
                # time-comparison of rects, like in Blocker trigger
                if (self.y_speed * game.gravity > 0) and (self.rect.y + 30 < block.rect.y):
                    if block.bouncy:
                        self.rect.bottom = block.rect.top
                        self.y_speed = -800 * game.gravity
                        self.bouncesound.play()
                    else:
                        self.y_speed = 0
                        self.rect.bottom = block.rect.top
                        self.resting = True  # Allows jump
                self.rect.x += block.xspeed * dt * block.direction
        # Test for collision with solid surfaces and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'blocker'):
            blockers = cell['blocker']
            if 'l' in blockers and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.bounced = False
                self.rect.right = cell.left
                if game.glitches["wallclimb"]:
                    if game.gravity == 1:
                        self.y_speed = -200
                    else:
                        self.y_speed = 200
            if 'r' in blockers and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.bounced = False
                self.rect.left = cell.right
                if game.glitches["wallclimb"]:
                    if game.gravity == 1:
                        self.y_speed = -200
                    else:
                        self.y_speed = 200
            if 't' in blockers and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                # Framework for clip-on-command glitch
                self.bounced = False
                if game.glitches["cliponcommand"]:
                    if not key[self.keys["down"]]:
                        self.rect.bottom = cell.top
                        if game.glitches["stickyceil"]:
                            self.y_speed = 3/dt
                        else:
                            self.y_speed = 0
                        if game.gravity == 1:
                            self.resting = True
                else:
                    self.rect.bottom = cell.top
                    if not key[self.keys["down"]]:
                        if game.glitches["stickyceil"]:
                            self.y_speed = 3/dt
                        else:
                            self.y_speed = 0
                    if game.gravity == 1:
                        self.resting = True
            if 'b' in blockers and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                # Part of the clip-on-command glitch Framework
                self.bounced = False
                if game.glitches["cliponcommand"]:
                    if not key[self.keys["down"]]:
                        self.rect.top = cell.bottom
                        if game.glitches["stickyceil"]:
                            self.y_speed = -5/dt
                        else:
                            self.y_speed = 0
                else:
                    self.rect.top = cell.bottom
                    if not key[self.keys["down"]]:
                        if game.glitches["stickyceil"]:
                            self.y_speed = -5/dt
                        else:
                            self.y_speed = 0
                if game.gravity == -1:
                    self.resting = True
        # ^--------------------------------------------------------------^
        # Test for collision with bouncy platforms and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers["Triggers"].collide(self.rect,
                                                            'bouncy'):
            bouncy = cell["bouncy"]
            power = int(cell["power"])
            if 't' in bouncy and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.bouncesound.play()
                self.rect.bottom = cell.top
                if game.gravity == 1:
                    self.y_speed = - power*game.gravity
                elif game.gravity == -1:
                    self.y_speed = power*game.gravity
            if 'b' in bouncy and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.bouncesound.play()
                self.rect.top = cell.bottom
                if game.gravity == 1:
                    self.y_speed = power*game.gravity
                elif game.gravity == -1:
                    self.y_speed = - power*game.gravity
            if 'l' in bouncy and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.bouncesound.play()
                self.bounced = True
                self.rect.right = cell.left
                self.x_speed = -power*dt
                if self.y_speed < 0:
                    self.y_speed = - game.gravity*power
                else:
                    self.y_speed = game.gravity*power
            if 'r' in bouncy and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.bouncesound.play()
                self.bounced = True
                self.rect.left = cell.right
                self.x_speed = power*dt
                if self.y_speed < 0:
                    self.y_speed = - game.gravity*power
                else:
                    self.y_speed = game.gravity*power
        # ^--------------------------------------------------------------^
        # Test for collisions with deadly ground and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers["Triggers"].collide(self.rect,
                                                            'deadly'):
            deadly = cell["deadly"]
            # FIXME: Can cross dead bodies horizontally
            # FIX: Bodies will be pretty thin, so i think i can ignore this
            if 't' in deadly and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.rect.bottom = cell.top
                self.respawn(game)
            if 'b' in deadly and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.rect.top = cell.bottom
                self.respawn(game)
            if 'l' in deadly and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.rect.right = cell.left
                self.respawn(game)
            if 'r' in deadly and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.rect.left = cell.right
                self.respawn(game)
        # ^--------------------------------------------------------------^
        # Test for collision with deadbody platforms and act accordingly
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.deadbodies, False)
        for block in collision:
            if self.y_speed == 0:
                self.resting = True
            elif self.y_speed * game.gravity > 0:
                self.rect.bottom = block.rect.top
                self.resting = True
                self.y_speed = 0
            # elif self.y_speed * game.gravity < 0:
            #    self.rect.top = block.rect.bottom
            #    self.resting = False
            #    self.y_speed = 0
        # ^--------------------------------------------------------------^
        # If help writings are solid, test for collision and act as platforms
        # v--------------------------------------------------------------v
        if game.glitches['solidhelp']:
            collision = pygame.sprite.spritecollide(self, game.helptxts, False)
            for block in collision:
                if self.y_speed == 0:
                    self.resting = True
                elif self.y_speed > 0 and game.gravity == 1:
                    self.rect.bottom = block.rect.top
                    self.resting = True
                    self.y_speed = 0
                elif self.y_speed < 0 and game.gravity == -1:
                    self.rect.top = block.rect.bottom
                    self.resting = False
                    self.y_speed = 0
        # ^--------------------------------------------------------------^
        # Test collision with help triggers and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'Help'):
            helptext = cell['Help']
            if helptext != game.getHelpText():
                game.setHelpFlag(False)
            if not game.getHelpFlag():
                game.setHelpFlag(True)
                game.setHelpText(helptext)
                x, y = game.tilemap.pixel_from_screen(cell.px+cell.width/2,
                                                      cell.py-20)
                Help(x, y, game.sprites, game=game, Text=helptext)
        # ^--------------------------------------------------------------^
        # Test collision with exit trigger and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'playerExit'):
            game.loadNextLevel(game.currentcampaign, game.screen)
            game.loadLevelPart2(game.keys)
        # ^--------------------------------------------------------------^
        game.tilemap.set_focus(self.rect.x, self.rect.y)    # Sets screen focus
        game.backpos[0] = -game.tilemap.view_x      # Moves background?
        # Wraps player movement if the glitch is active
        # v--------------------------------------------------------------v
        if game.glitches["hwrapping"]:
            # This piece of code should avoid phasing through the floor
            # v-----------------------------v
            if self.rect.x < 0:
                self.rect.x = game.tilemap.px_width - self.rect.width
                self.rect.y -= 3
            elif self.rect.x > game.tilemap.px_width:
                self.rect.x = 0
                self.rect.y -= 3
            # ^-----------------------------^
        if game.glitches["vwrapping"]:
            self.rect.y = self.rect.y % game.tilemap.px_height
        else:
            if self.rect.y < 0 or self.rect.y > game.tilemap.px_height:
                self.respawn(game)
        # ^--------------------------------------------------------------^
        # Handles the triggering of mobile platforms
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            "button"):
            if key[self.keys["down"]]:
                butt = cell['button']
                print(butt)
                for plat in game.plats:
                    if plat.id == butt:
                        plat.active = True
                        plat.image = plat.activeimg
        # ^--------------------------------------------------------------^
        # Handles the Glitched Area animations
        # v--------------------------------------------------------------v
        self.glitched = False
        for cell in game.tilemap.layers['Triggers'].collide(
                self.rect, "GlitchedAnimation"):
            self.glitched = True
        self.animate(self.y_speed, self.x_speed, self.resting, self.direction,
                     dt, game.gravity, self.running, self.glitched)
