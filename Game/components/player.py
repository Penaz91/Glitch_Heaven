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
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
mod_logger.addHandler(fh)
mod_logger.addHandler(ch)


class Player(pygame.sprite.Sprite):
    """ Class representing the player """
    size = (32, 32)     # Might be removed in future+taken from img
    runmultiplier = 2

    def toggleDoubleSpeed(self):
        self.playermaxspeed = 350
        self.playeraccel = 100

    def untoggleDoubleSpeed(self):
        self.playermaxspeed = 200
        self.playeraccel = 50

    def __init__(self, location, *groups, keys, game, sounds):
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
        self.playermaxspeed = 250
        self.playeraccel = 50
        self.active = True
        self.glitched = False
        self.soundslink = sounds
        self.jumpsound = sounds["sfx"]["jump"]
        self.deathsound = sounds["sfx"]["death"]
        self.bouncesound = sounds["sfx"]["bounce"]
        """self.idleani = timedanimation.TimedAnimation([0.25, 0.25, 0.25,
                                                      0.25, 0.25])"""
        self.idleani = timedanimation.TimedAnimation([0.25]*5)
        self.idleani.loadFromDir(os.path.join("resources",
                                              "sprites",
                                              "Player",
                                              "Idle"))
        """self.gidleani = timedanimation.TimedAnimation([0.25, 0.25, 0.25,
                                                      0.25, 0.25])"""
        self.gidleani = timedanimation.TimedAnimation([0.25]*5)
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
        self.jump_speed = -650
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
        """self.walkanimation = timedanimation.TimedAnimation([0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06])"""
        self.walkanimation = timedanimation.TimedAnimation([0.06]*10)
        self.walkanimation.loadFromDir(os.path.join("resources",
                                                    "sprites",
                                                    "Player",
                                                    "Walking"))
        """self.runanimation = timedanimation.TimedAnimation([0.04, 0.04, 0.04,
                                                           0.04, 0.04, 0.04,
                                                           0.04, 0.04])"""
        self.runanimation = timedanimation.TimedAnimation([0.04]*8)
        self.runanimation.loadFromDir(os.path.join("resources",
                                                   "sprites",
                                                   "Player",
                                                   "Running"))
        """self.gwalkanimation = timedanimation.TimedAnimation([0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06, 0.06, 0.06,
                                                            0.06])"""
        self.gwalkanimation = timedanimation.TimedAnimation([0.06]*10)
        self.gwalkanimation.loadFromDir(os.path.join("resources",
                                                     "sprites",
                                                     "Glitched_Player",
                                                     "Walking"))
        """self.grunanimation = timedanimation.TimedAnimation([0.04, 0.04, 0.04,
                                                           0.04, 0.04, 0.04,
                                                           0.04, 0.04])"""
        self.grunanimation = timedanimation.TimedAnimation([0.04]*8)
        self.grunanimation.loadFromDir(os.path.join("resources",
                                                    "sprites",
                                                    "Glitched_Player",
                                                    "Running"))
        self.pushimg = pygame.image.load(
                os.path.join("resources",
                             "sprites",
                             "Player",
                             "Pushing.png")).convert_alpha()
        self.particles = pygame.sprite.Group()
        self.game = game
        self.running = False
        self.pushing = False
        if game.config.getboolean("Video", "playerparticles"):
            self.leftemitter = emitter.Emitter(self.rect.bottomleft,
                                               (0, 255, 84),
                                               (0, 103, 34), -1, -1,
                                               self.particles,
                                               game.tilemap)
            self.rightemitter = emitter.Emitter(self.rect.bottomright,
                                                (0, 255, 84),
                                                (0, 103, 34), 1, -1,
                                                self.particles,
                                                game.tilemap)
        self.lastcheckpoint = location

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
        if self.active:
            x, y = game.tilemap.pixel_from_screen(self.rect.x,
                                                  self.rect.y)
            mod_logger.info("Player respawned, position of death: (" +
                            str(x) + "," + str(y) + ")")
            if game.glitches["permBodies"]:
                body = DeadBody(x, y, game.sprites, game=game)
                game.deadbodies.add(body)
            if game.glitches["invertedGravity"]:
                game.gravity = -1
            else:
                game.gravity = 1
            self.deathsound.play()
            # ^-----------------------------------------------------^
            # Does a complete respawn of the player
            # v-----------------------------------------------------v
            game.player.rect.x, game.player.rect.y = self.lastcheckpoint
            game.player.y_speed = 0
            game.player.x_speed = 0
            # ^-----------------------------------------------------^
            game.deathCounter += 1

    def animate(self, yspeed, xspeed, resting,
                direction, dt, gravity, running, pushing, glitched):
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
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.leftemitter.move(self.rect.bottomleft)
                                else:
                                    self.leftemitter.move(self.rect.topleft)
                                self.leftemitter.emit(2, 2*gravity)
                            self.image = self.grunanimation.next(dt)
                        else:
                            # Player is walking rightwards
                            self.image = self.gwalkanimation.next(dt)
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.leftemitter.move(self.rect.bottomleft)
                                else:
                                    self.leftemitter.move(self.rect.topleft)
                                self.leftemitter.emit(1, gravity)
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
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.rightemitter.move(
                                            self.rect.bottomright)
                                else:
                                    self.rightemitter.move(self.rct.topright)
                                self.rightemitter.emit(2, 2*gravity)
                        else:
                            # Player is walking leftwards
                            self.image = pygame.transform.flip(
                                         self.gwalkanimation.next(dt),
                                         True,
                                         False)
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.rightemitter.move(
                                            self.rect.bottomright)
                                else:
                                    self.rightemitter.move(self.rct.topright)
                                self.rightemitter.emit(1, gravity)
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
                        if pushing:
                            self.image = self.pushimg
                        elif running:
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.leftemitter.move(self.rect.bottomleft)
                                else:
                                    self.leftemitter.move(self.rect.topleft)
                                self.leftemitter.emit(2, 2*gravity)
                            # Player is running rightwards
                            self.image = self.runanimation.next(dt)
                        else:
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.leftemitter.move(self.rect.bottomleft)
                                else:
                                    self.leftemitter.move(self.rect.topleft)
                                self.leftemitter.emit(1, gravity)
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
                        if pushing:
                            self.image = pygame.transform.flip(
                                         self.pushimg,
                                         True,
                                         False)
                        elif running:
                            # Player is running leftwards
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.rightemitter.move(
                                            self.rect.bottomright)
                                else:
                                    self.rightemitter.move(self.rect.topright)
                                self.rightemitter.emit(2, 2*gravity)
                            self.image = pygame.transform.flip(
                                         self.runanimation.next(dt),
                                         True,
                                         False)
                        else:
                            # Player is walking leftwards
                            if self.game.config.getboolean("Video",
                                                           "playerparticles"):
                                if gravity == 1:
                                    self.rightemitter.move(
                                            self.rect.bottomright)
                                else:
                                    self.rightemitter.move(self.rect.topright)
                                self.rightemitter.emit(1, gravity)
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
        if game.glitches["invertedRun"]:
            self.running = not bool(key[self.keys["run"]])
        else:
            self.running = bool(key[self.keys["run"]])
        if game.glitches["invertedControls"]:
            self.left = key[self.keys["right"]]
            self.right = key[self.keys["left"]]
        else:
            self.left = key[self.keys["left"]]
            self.right = key[self.keys["right"]]
        if self.left and not game.glitches["noLeft"]:
            self.direction = -1     # Mainly for different bounce mechanics
            if not self.bounced:        # Not bounced away -> control in air
                # Why do i have different control in air if i'm running?
                # This might lead to a change of speed in air
                # Do i want this?
                # v--------------------------------------------------------v
                if self.running:
                    self.x_speed = max(-self.playermaxspeed * dt *
                                       self.runmultiplier,
                                       self.x_speed-self.playeraccel*dt *
                                       self.runmultiplier)  # Use running speed
                # ^--------------------------------------------------------^
                else:
                    self.x_speed = max(-self.playermaxspeed * dt,
                                       self.x_speed -
                                       self.playeraccel*dt)  # Use walk speed
        elif self.right and not game.glitches["noRight"]:
            if not self.bounced:
                self.direction = 1  # Used mainly for bouncy mechanics
                if self.running:
                    self.x_speed = min(self.playermaxspeed * dt *
                                       self.runmultiplier,
                                       self.x_speed+self.playeraccel * dt *
                                       self.runmultiplier)  # Use run speed
                else:
                    self.x_speed = min(self.playermaxspeed*dt,
                                       self.x_speed +
                                       self.playeraccel*dt)  # Walk Speed
        else:
            # Gives the player some control over the fall if they're not
            # bounced away from a spring
            # TODO: Find some better way to let player keep control
            # TODO: Tie direction and movement in a formula instead of conds
            # v--------------------------------------------------------------v
            if game.glitches["noStop"]:
                if self.x_speed != 0:
                    if self.running:
                        self.x_speed = self.playermaxspeed *\
                                self.direction * self.runmultiplier * dt
                    else:
                        self.x_speed = self.playermaxspeed *\
                                self.direction * dt
            else:
                if not self.bounced:
                    if self.direction == 1:
                        self.x_speed = max(0,
                                           self.x_speed-(self.playeraccel*dt))
                    elif self.direction == -1:
                        self.x_speed = min(0,
                                           self.x_speed+(self.playeraccel*dt))
            # ^--------------------------------------------------------------^
        self.rect.x += self.x_speed         # Move the player
        if game.glitches["multiJump"]:
            if key[self.keys["jump"]] and not game.glitches["noJump"]:
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
                        if game.glitches["highJump"]:
                            self.y_speed = self.jump_speed*2*game.gravity
                        else:
                            self.y_speed = self.jump_speed*game.gravity
                        if game.config.getboolean("Video", "playerparticles"):
                            if game.gravity == 1:
                                self.rightemitter.move(self.rect.bottomright)
                                self.leftemitter.move(self.rect.bottomleft)
                            else:
                                self.rightemitter.move(self.rect.topright)
                                self.leftemitter.move(self.rect.topleft)
                            self.rightemitter.emit(1, game.gravity)
                            self.leftemitter.emit(1, game.gravity)
                    # ^------------------------------------------------------^
        elif game.glitches["hover"]:
            if key[self.keys["jump"]] and not game.glitches["noJump"]:
                if self.y_speed == 0:
                    self.jumpsound.play()
                self.y_speed = self.jump_speed*game.gravity*0.8
                if game.config.getboolean("Video", "playerparticles"):
                    if game.gravity == 1:
                        self.rightemitter.move(self.rect.bottomright)
                        self.leftemitter.move(self.rect.bottomleft)
                    else:
                        self.rightemitter.move(self.rect.topright)
                        self.leftemitter.move(self.rect.topleft)
                    self.rightemitter.emit(1, game.gravity)
                    self.leftemitter.emit(1, game.gravity)
        else:
            if key[self.keys["jump"]] and self.resting and\
                    not game.glitches["noJump"]:
                self.jumpsound.play()
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    # If the high jump glitch is active, jumps twice as high
                    # v------------------------------------------------------v
                    if game.glitches["highJump"]:
                        self.y_speed = self.jump_speed*2*game.gravity
                    else:
                        self.y_speed = self.jump_speed*game.gravity
                    if game.config.getboolean("Video", "playerparticles"):
                        if game.gravity == 1:
                            self.rightemitter.move(self.rect.bottomright)
                            self.leftemitter.move(self.rect.bottomleft)
                        else:
                            self.rightemitter.move(self.rect.topright)
                            self.leftemitter.move(self.rect.topleft)
                        self.rightemitter.emit(1, game.gravity)
                        self.leftemitter.emit(1, game.gravity)
                        # ^------------------------------------------------------^
                    self.resting = False    # I jumped, so i'm not on a surface
        if game.glitches["featherFalling"]:
            if game.glitches["ledgeJump"]:
                if game.gravity == 1:
                    self.y_speed = (min(350, self.y_speed+35))
                elif game.gravity == -1:
                    self.y_speed = max(-350, self.y_speed-35)
            else:
                if game.gravity == 1:
                    self.y_speed = (min(350, self.y_speed+35))
                elif game.gravity == -1:
                    self.y_speed = max(-350, self.y_speed-35)
        else:
            if game.glitches["ledgeJump"]:
                if game.gravity == 1:
                    self.y_speed = (min(600, self.y_speed+60))
                elif game.gravity == -1:
                    self.y_speed = max(-600, self.y_speed-60)
            else:
                if game.gravity == 1:
                    self.y_speed = (min(600, self.y_speed+60))
                elif game.gravity == -1:
                    self.y_speed = max(-600, self.y_speed-60)
        if game.glitches['ledgeWalk']:
            if not self.resting:
                self.rect.y += self.y_speed * dt   # Move the player vertically
        else:
            self.rect.y += self.y_speed * dt    # Move the player vertically
        # This avoids the ability to jump in air after leaving a platform
        # + ledgejump glitch framework
        # v--------------v
        if not game.glitches["ledgeJump"] and not game.glitches["ledgeWalk"]:
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
                if self.y_speed * game.gravity > 0:
                    if game.gravity == 1 and self.rect.bottom > block.rect.top:
                        self.rect.bottom = block.rect.top
                        if block.bouncy:
                            self.y_speed = - block.bouncepwr
                            self.bouncesound.play()
                        else:
                            self.y_speed = block.yspeed
                            self.resting = True  # Allows jump
                    elif game.gravity == -1 and\
                            self.rect.top < block.rect.bottom:
                        self.rect.top = block.rect.bottom
                        if block.bouncy:
                            self.y_speed = block.bouncepwr
                            self.bouncesound.play()
                        else:
                            self.y_speed = - block.yspeed
                            self.resting = True  # Allows jump
                if block.moving:
                    self.rect.x += block.xspeed * dt * block.direction
        # Test for collision with scrolling ground
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'slide'):
            slide = int(cell['slide'])
            if game.glitches["slideInvert"]:
                if key[self.keys["action"]]:
                    slide *= -1
            self.rect.x += slide * dt
        # ^--------------------------------------------------------------^
        # Test for collision with deadbody platforms and act accordingly
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.deadbodies, False)
        for block in collision:
            if self.y_speed == 0:
                self.resting = True
            elif self.y_speed * game.gravity > 0:
                if game.gravity == 1:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom
                self.resting = True
                self.y_speed = 0
        # ^--------------------------------------------------------------^
        # Test for collision with solid surfaces and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'blocker'):
            blockers = cell['blocker']
            self.pushing = False
            if 't' in blockers and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                # Framework for clip-on-command glitch
                self.bounced = False
                if game.glitches["clipOnCommand"]:
                    if not key[self.keys["action"]]:
                        self.rect.bottom = cell.top
                        if game.glitches["stickyCeil"]:
                            self.y_speed = 3/dt
                        else:
                            self.y_speed = 0
                        if game.gravity == 1:
                            self.resting = True
                else:
                    self.rect.bottom = cell.top
                    if not key[self.keys["action"]]:
                        if game.glitches["stickyCeil"]:
                            self.y_speed = 3/dt
                        else:
                            self.y_speed = 0
                    if game.gravity == 1:
                        self.resting = True
            elif 'b' in blockers and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                # Part of the clip-on-command glitch Framework
                self.bounced = False
                if game.glitches["clipOnCommand"]:
                    if not key[self.keys["action"]]:
                        self.rect.top = cell.bottom
                        if game.glitches["stickyCeil"]:
                            self.y_speed = -5/dt
                        # This has to stay to avoid an unwanted
                        # stickyceil effect
                        else:
                            self.y_speed = 0
                else:
                    self.rect.top = cell.bottom
                    if not key[self.keys["action"]]:
                        if game.glitches["stickyCeil"]:
                            self.y_speed = -5/dt
                        # This has to stay to avoid an unwanted
                        # stickyceil effect
                        else:
                            self.y_speed = 0
                if game.gravity == -1:
                    self.resting = True
            elif 'l' in blockers and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.bounced = False
                self.rect.right = cell.left
                self.pushing = True
                if game.glitches["wallClimb"]:
                    if game.gravity == 1:
                        self.y_speed = -200
                    else:
                        self.y_speed = 200
            # else:
                # self.pushing = False
            elif 'r' in blockers and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.bounced = False
                self.rect.left = cell.right
                self.pushing = True
                if game.glitches["wallClimb"]:
                    if game.gravity == 1:
                        self.y_speed = -200
                    else:
                        self.y_speed = 200
        # ^--------------------------------------------------------------^
        # Test for collision with bouncy platforms and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers["Triggers"].collide(self.rect,
                                                            'bouncy'):
            bouncy = cell["bouncy"]
            power = int(cell["power"])
            if 't' in bouncy and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.rect.bottom = cell.top
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    if game.gravity == 1:
                        self.y_speed = - power*game.gravity
                    elif game.gravity == -1:
                        self.y_speed = power*game.gravity
            if 'b' in bouncy and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.rect.top = cell.bottom
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    if game.gravity == 1:
                        self.y_speed = power*game.gravity
                    elif game.gravity == -1:
                        self.y_speed = - power*game.gravity
            if 'l' in bouncy and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.rect.right = cell.left
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    self.bounced = True
                    self.x_speed = -power*dt
                    if self.y_speed < 0:
                        self.y_speed = - game.gravity*power
                    else:
                        self.y_speed = game.gravity*power
            if 'r' in bouncy and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.rect.left = cell.right
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    self.bounced = True
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
        # If help writings are solid, test for collision and act as platforms
        # v--------------------------------------------------------------v
        if game.glitches['solidHelp']:
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
            game.loadNextLevel(game.campaignname, game.currentcampaign,
                               game.mode, game.screen)
            game.loadLevelPart2(game.keys, self.soundslink)
        # ^--------------------------------------------------------------^
        game.tilemap.set_focus(self.rect.x, self.rect.y)    # Sets screen focus
        game.backpos[0] = -game.tilemap.view_x      # Moves background?
        # Wraps player movement if the glitch is active
        # v--------------------------------------------------------------v
        if game.glitches["hWrapping"]:
            # This piece of code should avoid phasing through the floor
            # v-----------------------------v
            if self.rect.x < 0:
                self.rect.x = game.tilemap.px_width - self.rect.width
                self.rect.y -= 3
            elif self.rect.x > game.tilemap.px_width:
                self.rect.x = 0
                self.rect.y -= 3
            # ^-----------------------------^
        if game.glitches["vWrapping"]:
            self.rect.y = self.rect.y % game.tilemap.px_height
        else:
            if self.rect.y < 0 or self.rect.y > game.tilemap.px_height:
                self.respawn(game)
        # ^--------------------------------------------------------------^
        # Handles the triggering of mobile platforms
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            "button"):
            if key[self.keys["action"]]:
                butt = cell['button']
                mod_logger.info("Player pressed the button with ID: " +
                                str(butt))
                for plat in game.plats:
                    if plat.id == butt:
                        plat.active = True
                        plat.image = plat.activeimg
        # ^--------------------------------------------------------------^
        # Handles the triggering of teleporters
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            "TpIn"):
            if key[self.keys["action"]]:
                tpin = cell['TpIn']
                mod_logger.info("Player entered the TP with ID: " +
                                str(tpin))
                for out in game.tilemap.layers['Triggers'].find("TpOut"):
                    tpout = out['TpOut']
                    if tpout == tpin:
                        self.rect.x = out.px
                        self.rect.y = out.py
        # ^--------------------------------------------------------------^
        # Handles the Glitched Area animations
        # v--------------------------------------------------------------v
        self.glitched = False
        for cell in game.tilemap.layers['Triggers'].collide(
                self.rect, "GlitchedAnimation"):
            self.glitched = True
        # ^--------------------------------------------------------------^
        # Handles The checkpoints
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(
                self.rect, 'CheckPoint'):
                chk = cell['CheckPoint']
                if chk == 1:
                    self.lastcheckpoint = (self.rect.x, self.rect.y)
                    cell['CheckPoint'] = 0
                    mod_logger.info("Checkpoint Saved")
        # ^--------------------------------------------------------------^
        # Handles The Glitch Triggers
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self,
                                                game.GlitchTriggers,
                                                False)
        for block in collision:
            block.toggle(self.game)
            block.kill()
        # ^--------------------------------------------------------------^
        # Handles the glitchiness in Critical Failure mode
        # v--------------------------------------------------------------v
        if game.mode.lower() in ["criticalfailure", "cfsingle"]:
            redcoll = game.tilemap.pixel_to_screen(self.rect.x, self.rect.y)
            if redcoll[1] < game.redsurfrect.bottom:
                self.glitched = True
            else:
                self.glitched = False
        # ^--------------------------------------------------------------^
        # Handles the player plaform-like behaviour in case the ObsResistant
        # glitch is active, or its death
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.obstacles, False)
        for block in collision:
            if game.glitches["obsResistant"]:
                if self.y_speed * game.gravity > 0:
                    if game.gravity == 1 and self.rect.bottom > block.rect.top:
                        self.rect.bottom = block.rect.top
                        self.y_speed = block.yspeed
                        self.resting = True  # Allows jump
                    elif game.gravity == -1 and\
                            self.rect.top < block.rect.bottom:
                        self.rect.top = block.rect.bottom
                        self.y_speed = - block.yspeed
                        self.resting = True  # Allows jump
                self.rect.x += block.xspeed * dt * block.direction
            else:
                self.respawn(game)
        # MUST BE LAST OPERATION
        # v--------------------------------------------------------------v
        self.animate(self.y_speed, self.x_speed, self.resting, self.direction,
                     dt, game.gravity, self.running,
                     self.pushing, self.glitched)
