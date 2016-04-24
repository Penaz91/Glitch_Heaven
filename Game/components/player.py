# Player component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
#
# ------------------------------------------------
# TODO AREA
# - Reduce boilerplate concerning Common operations with left
#   and right movement.
# - Reduce boilerplate concerning the emission of particles
# - Tie player size to the size of the sprite
# - Tie bouncing mechanics directly to direction via formula,
#   instead of using conditionals, to save CPU power.
# ------------------------------------------------
import pygame
from os.path import join as pjoin
from components.deadbody import DeadBody
from components.help import Help
from libs.spritesheetanimation import SpritesheetAnimation as SpriteAni
from libs import emitter


class Player(pygame.sprite.Sprite):
    """ Class representing the player """
    _runpower_ = 2
    _jump_speed_ = -650
    _initialParticleColor_ = (0, 255, 84)
    _finalParticleColor_ = (0, 103, 34)

    def DoubleSpeedOn(self):
        self.playermaxspeed = 350
        self.playeraccel = 100

    def DoubleSpeedOff(self):
        self.playermaxspeed = 250
        self.playeraccel = 50

    def HiJumpOn(self):
        self.jumpMultiplier = 2

    def HiJumpOff(self):
        self.jumpMultiplier = 1

    def loadSprites(self):
        self.idleani = SpriteAni(0.25,
                                 pjoin("resources",
                                       "sprites",
                                       "Player",
                                       "Idle.png"))
        self.gidleani = SpriteAni(0.25,
                                  pjoin("resources",
                                        "sprites",
                                        "Glitched_Player",
                                        "Idle.png"))
        self.fallingsprite = pygame.image.load(
                pjoin("resources",
                      "sprites",
                      "Player",
                      "jump_fall.png")).convert_alpha()
        self.jumpsprite = pygame.image.load(
                pjoin("resources",
                      "sprites",
                      "Player",
                      "jump_rise.png")).convert_alpha()
        self.gfallingsprite = pygame.image.load(
                pjoin("resources",
                      "sprites",
                      "Glitched_Player",
                      "jump_fall.png")).convert_alpha()
        self.gjumpsprite = pygame.image.load(
                pjoin("resources",
                      "sprites",
                      "Glitched_Player",
                      "jump_rise.png")).convert_alpha()
        self.walkanimation = SpriteAni(0.06,
                                       pjoin("resources",
                                             "sprites",
                                             "Player",
                                             "Walking.png"))
        self.runanimation = SpriteAni(0.04,
                                      pjoin("resources",
                                            "sprites",
                                            "Player",
                                            "Running.png"))
        self.gwalkanimation = SpriteAni(0.06,
                                        pjoin("resources",
                                              "sprites",
                                              "Glitched_Player",
                                              "Walking.png"))
        self.grunanimation = SpriteAni(0.04,
                                       pjoin("resources",
                                             "sprites",
                                             "Glitched_Player",
                                             "Running.png"))
        self.pushimg = pygame.image.load(
                pjoin("resources",
                      "sprites",
                      "Player",
                      "Pushing.png")).convert_alpha()
        self.bounced = SpriteAni(0.04,
                                 pjoin("resources",
                                       "sprites",
                                       "Player",
                                       "Bounced.png"))
        self.gpushimg = pygame.image.load(
                pjoin("resources",
                      "sprites",
                      "Glitched_Player",
                      "Pushing.png")).convert_alpha()
        self.gbounced = SpriteAni(0.04,
                                  pjoin("resources",
                                        "sprites",
                                        "Glitched_Player",
                                        "Bounced.png"))
        self.normalSprite = {
            "idle": self.idleani,
            "walk": self.walkanimation,
            "run": self.runanimation,
            "bounced": self.bounced,
            "jump_rise": self.jumpsprite,
            "jump_fall": self.fallingsprite,
            "push": self.pushimg
        }
        self.glitchedSprite = {
            "idle": self.gidleani,
            "walk": self.gwalkanimation,
            "run": self.grunanimation,
            "bounced": self.gbounced,
            "jump_rise": self.gjumpsprite,
            "jump_fall": self.gfallingsprite,
            "push": self.gpushimg
        }

    def setupEmitters(self):
        if self.game.config.getboolean("Video", "playerparticles"):
            self.leftemitter = emitter.Emitter(self.rect.bottomleft,
                                               self._initialParticleColor_,
                                               self._finalParticleColor_,
                                               -1, -1,
                                               self.particles,
                                               self.game.tilemap)
            self.rightemitter = emitter.Emitter(self.rect.bottomright,
                                                self._initialParticleColor_,
                                                self._finalParticleColor_,
                                                1, -1,
                                                self.particles,
                                                self.game.tilemap)

    def emit_Right(self):
        if self.game.gravity == 1:
            self.rightemitter.move(self.rect.bottomright)
        else:
            self.rightemitter.move(self.rect.topright)
        self.rightemitter.emit(self.runmultiplier,
                               self.runmultiplier*self.game.gravity)

    def emit_Left(self):
        if self.game.gravity == 1:
            self.leftemitter.move(self.rect.bottomleft)
        else:
            self.leftemitter.move(self.rect.topleft)
        self.leftemitter.emit(self.runmultiplier,
                              self.runmultiplier*self.game.gravity)

    def __init__(self, location, *groups, keys, game, sounds, log):
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
        self.mod_logger = log.getChild("playerEntity")
        self.playermaxspeed = 250
        self.playeraccel = 50
        self.runmultiplier = 1
        self.glitched = False
        self.jumpMultiplier = 1
        self.soundslink = sounds
        self.jumpsound = sounds["sfx"]["jump"]
        self.deathsound = sounds["sfx"]["death"]
        self.bouncesound = sounds["sfx"]["bounce"]
        self.loadSprites()
        self.image = self.idleani.currentframe
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.x, self.rect.y = location
        self.resting = False
        self.x_speed, self.y_speed = 0, 0
        self.direction = 1      # 1=Right, -1=Left
        self.bounced = False    # Used to ignore input when bounced
        self.keys = keys
        self.particles = pygame.sprite.Group()
        self.game = game
        self.running = False
        self.pushing = False
        self.setupEmitters()
        self.lastcheckpoint = location
        self.collisionrect = pygame.rect.Rect((0, 0), (20, 32))
        self.collisionrect.midbottom = self.rect.midbottom

    def respawn(self, game):
        """
        Method used to respawn the player after death

        Keyword Arguments:
        - game: The game instance

        Returns:
        - Nothing
        """
        # If the permbody glitch is active, will add a body at death position
        # v-----------------------------------------------------v
        # if self.active:
        x, y = game.tilemap.pixel_from_screen(self.rect.x,
                                              self.rect.y)
        self.mod_logger.info("Player respawned, death coords: (%(x)s, %(y)s)"
                             % locals())
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
        game.player.x_speed, game.player.y_speed = 0, 0
        # ^-----------------------------------------------------^
        if not game.glitches["permBodies"]:
            game.deathCounter += 1

    def animate(self, yspeed, xspeed, resting, bounced,
                direction, dt, gravity, running, pushing, glitched, game):
        spriteList = None
        if glitched:
            spriteList = self.glitchedSprite
        else:
            spriteList = self.normalSprite
        if resting:
            # IDLE - Walk - Run code
            if xspeed == 0:
                # Player is idle
                self.image = spriteList["idle"].next(dt)
            else:
                if pushing:
                    self.image = spriteList["push"]
                elif running:
                    self.image = spriteList["run"].next(dt)
                else:
                    self.image = spriteList["walk"].next(dt)
        elif bounced:
            # Bounced Animation
            self.image = spriteList["bounced"].next(dt)
        else:
            # Jump - Fall Animation
            if yspeed * gravity > 0:
                self.image = spriteList["jump_fall"]
            elif yspeed * gravity < 0:
                self.image = spriteList["jump_rise"]
        # Image Flipping
        self.image = pygame.transform.flip(self.image, (direction == -1),
                                           (gravity == -1))
        if game.modifiers["moonwalk"]:
            self.image = pygame.transform.flip(
                         self.image, True, False)
        # Particle emission
        if self.game.config.getboolean("Video", "playerparticles"):
            if(xspeed != 0 and resting) and not pushing:
                if direction == 1:
                    self.emit_Left()
                else:
                    self.emit_Right()

    def emitJumpParticles(self):
        if self.game.gravity == 1:
            self.rightemitter.move(self.rect.bottomright)
            self.leftemitter.move(self.rect.bottomleft)
        else:
            self.rightemitter.move(self.rect.topright)
            self.leftemitter.move(self.rect.topleft)
        self.rightemitter.emit(1, self.game.gravity)
        self.leftemitter.emit(1, self.game.gravity)

    def update(self, dt, game):
        """
        Updates the status of the player

        Keyword Arguments:
        - dt: The time slice (clock.tick())
        - game: The Game instance.

        Returns:
        - Nothing
        """
        if game.gravity == 1:
            self.collisionrect.midbottom = self.rect.midbottom
        else:
            self.collisionrect.midtop = self.rect.midtop
        last = self.collisionrect.copy()  # Copy last position for compare
        key = pygame.key.get_pressed()
        # Check if run button is pressed (With eventual Invertedrun glitch)
        # v--------------------------------------------------------------v
        if game.glitches["invertedRun"]:
            self.running = not bool(key[self.keys["run"]])
        else:
            self.running = bool(key[self.keys["run"]])
        # ^--------------------------------------------------------------^
        if self.running:
            self.runmultiplier = self._runpower_
        else:
            self.runmultiplier = 1
        # Check if Left/Right buttons are pressed
        # (W/ eventual Invertedcontrols glitch)
        # v--------------------------------------------------------------v
        if game.glitches["invertedControls"]:
            self.left = key[self.keys["right"]]
            self.right = key[self.keys["left"]]
        else:
            self.left = key[self.keys["left"]]
            self.right = key[self.keys["right"]]
        # ^--------------------------------------------------------------^
        if self.left and not game.glitches["noLeft"]:
            self.direction = -1     # Mainly for different bounce mechanics
            if not self.bounced:        # Not bounced away -> control in air
                # Why do i have different control in air if i'm running?
                # This might lead to a change of speed in air
                # Do i want this?
                # v--------------------------------------------------------v
                self.x_speed = max(-self.playermaxspeed * dt *
                                   self.runmultiplier,
                                   self.x_speed-self.playeraccel*dt *
                                   self.runmultiplier)  # Use run/walk speed
                # ^--------------------------------------------------------^
        elif self.right and not game.glitches["noRight"]:
            self.direction = 1  # Used mainly for bouncy mechanics
            if not self.bounced:
                self.x_speed = min(self.playermaxspeed * dt *
                                   self.runmultiplier,
                                   self.x_speed+self.playeraccel * dt *
                                   self.runmultiplier)  # Use run/walk speed
        else:
            # Gives the player some control over the fall if they're not
            # bounced away from a spring
            # TODO: Find some better way to let player keep control
            # TODO: Tie direction and movement in a formula instead of conds
            # v--------------------------------------------------------------v
            if game.glitches["noStop"]:
                if self.x_speed != 0:
                    self.x_speed = self.playermaxspeed *\
                            self.direction * self.runmultiplier * dt
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
        if game.gravity == 1:
            self.collisionrect.midbottom = self.rect.midbottom
        else:
            self.collisionrect.midtop = self.rect.midtop
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
                    if self.y_speed*game.gravity > -(self._jump_speed_/2) or\
                            self.resting:
                        self.y_speed = self._jump_speed_ * \
                           self.jumpMultiplier * game.gravity
                        if game.config.getboolean("Video", "playerparticles"):
                            self.emitJumpParticles()
                    # ^------------------------------------------------------^
        elif game.glitches["hover"]:
            if key[self.keys["jump"]] and not game.glitches["noJump"]:
                if self.resting:
                    self.jumpsound.play()
                self.y_speed = self._jump_speed_*game.gravity*0.8
                if game.config.getboolean("Video", "playerparticles"):
                    self.emitJumpParticles()
        else:
            if key[self.keys["jump"]] and self.resting and\
                    not game.glitches["noJump"]:
                self.jumpsound.play()
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    # If the high jump glitch is active, jumps twice as high
                    # v------------------------------------------------------v
                    self.y_speed = self._jump_speed_ * \
                            self.jumpMultiplier * game.gravity
                    if game.config.getboolean("Video", "playerparticles"):
                        self.emitJumpParticles()
                        # ^------------------------------------------------------^
                    self.resting = False    # I jumped, so i'm not on a surface
        if game.glitches["featherFalling"]:
            if game.gravity == 1:
                self.y_speed = (min(350, self.y_speed+35))
            elif game.gravity == -1:
                self.y_speed = max(-350, self.y_speed-35)
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
        if game.gravity == 1:
            self.collisionrect.midbottom = self.rect.midbottom
        else:
            self.collisionrect.midtop = self.rect.midtop

        # This avoids the ability to jump in air after leaving a platform
        # + ledgejump glitch framework
        # v--------------v
        if not game.glitches["ledgeJump"] and not game.glitches["ledgeWalk"]:
            self.resting = False
        # ^--------------^
        # Test for collision with scrolling ground
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'slide'):
            top = last.bottom <= cell.top and\
                  self.collisionrect.bottom > cell.top
            bottom = last.top >= cell.bottom and\
                self.collisionrect.top < cell.bottom
            if top or bottom:
                slide = int(cell['slide'])
                if game.glitches["slideInvert"]:
                    if key[self.keys["action"]]:
                        slide *= -1
                self.rect.x += slide * dt
                self.collisionrect.midbottom = self.rect.midbottom
        # ^--------------------------------------------------------------^
        # Test for collision with deadbody platforms and act accordingly
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.deadbodies, False)
        for block in collision:
            if game.gravity == 1:
                if last.bottom <= block.rect.top and\
                        self.collisionrect.bottom > block.rect.top:
                    self.rect.bottom = block.rect.top
                    self.resting = True
                    self.y_speed = 0
            else:
                if last.top >= block.rect.bottom and\
                        self.collisionrect.top < block.rect.bottom:
                    self.rect.top = block.rect.bottom
                    self.resting = True
                    self.y_speed = 0
        # ^--------------------------------------------------------------^
        if game.glitches["vWrapping"]:
            if self.rect.y < 0:
                last.y = game.tilemap.px_height + 32
                self.rect.y = game.tilemap.px_height
            elif self.rect.y > game.tilemap.px_height:
                last.y = -32
                self.rect.y = 0
            self.collisionrect.midbottom = self.rect.midbottom
        else:
            if self.rect.y < 0 or self.rect.y > game.tilemap.px_height:
                self.respawn(game)
        # ^--------------------------------------------------------------^
        # Moving plats collision check
        # NOTE: This has to stay here to avoid being tped under a platform
        #       if you touch a vertical wall
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.plats, False)
        for block in collision:
            if block.active:
                if game.gravity == 1:
                    if last.bottom <= block.last.top and\
                            self.collisionrect.bottom > block.rect.top:
                        self.rect.bottom = block.rect.top
                        if block.bouncy:
                            self.y_speed = - block.bouncepwr
                            self.bouncesound.play()
                        else:
                            self.y_speed = block.yspeed
                            self.resting = True  # Allows jump
                else:
                    if last.top >= block.last.bottom and\
                           self.collisionrect.top < block.rect.bottom:
                        self.rect.top = block.rect.bottom
                        if block.bouncy:
                            self.y_speed = block.bouncepwr
                            self.bouncesound.play()
                        else:
                            self.y_speed = - block.yspeed
                            self.resting = True  # Allows jump
                if block.moving:
                    self.rect.x += block.xspeed * dt * block.direction
        self.collisionrect.midbottom = self.rect.midbottom
        # Test for collision with solid surfaces and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'blocker'):
            blockers = cell['blocker']
            self.pushing = False
            if 't' in blockers and last.bottom <= cell.top and\
                    self.collisionrect.bottom > cell.top:
                # Framework for clip-on-command glitch
                self.bounced = False
                if game.glitches["clipOnCommand"]:
                    if not key[self.keys["action"]]:
                        self.collisionrect.bottom = cell.top
                        if game.glitches["stickyCeil"]:
                            self.y_speed = 3/dt
                        else:
                            self.y_speed = 0
                        if game.gravity == 1:
                            self.resting = True
                else:
                    self.collisionrect.bottom = cell.top
                    if not key[self.keys["action"]]:
                        if game.glitches["stickyCeil"]:
                            self.y_speed = 3/dt
                        else:
                            self.y_speed = 0
                    if game.gravity == 1:
                        self.resting = True
            elif 'b' in blockers and last.top >= cell.bottom and\
                    self.collisionrect.top < cell.bottom:
                # Part of the clip-on-command glitch Framework
                self.bounced = False
                if game.glitches["clipOnCommand"]:
                    if not key[self.keys["action"]]:
                        self.collisionrect.top = cell.bottom
                        if game.glitches["stickyCeil"]:
                            self.y_speed = -5/dt
                        # This has to stay to avoid an unwanted
                        # stickyceil effect
                        else:
                            self.y_speed = 0
                else:
                    self.collisionrect.top = cell.bottom
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
                    self.collisionrect.right > cell.left:
                self.bounced = False
                self.collisionrect.right = cell.left
                self.pushing = True
                if game.glitches["wallClimb"]:
                    if game.gravity == 1:
                        self.y_speed = -200
                    else:
                        self.y_speed = 200
            elif 'r' in blockers and last.left >= cell.right and\
                    self.collisionrect.left < cell.right:
                self.bounced = False
                self.collisionrect.left = cell.right
                self.pushing = True
                if game.glitches["wallClimb"]:
                    if game.gravity == 1:
                        self.y_speed = -200
                    else:
                        self.y_speed = 200
            self.rect.midbottom = self.collisionrect.midbottom
        # ^--------------------------------------------------------------^
        # Test for collision with bouncy platforms and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers["Triggers"].collide(self.collisionrect,
                                                            'bouncy'):
            bouncy = cell["bouncy"]
            power = int(cell["power"])
            if 't' in bouncy and last.bottom <= cell.top and\
                    self.collisionrect.bottom > cell.top:
                self.rect.bottom = cell.top
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    if game.gravity == 1:
                        self.y_speed = - power*game.gravity
                    elif game.gravity == -1:
                        self.y_speed = power*game.gravity
            if 'b' in bouncy and last.top >= cell.bottom and\
                    self.collisionrect.top < cell.bottom:
                self.rect.top = cell.bottom
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    if game.gravity == 1:
                        self.y_speed = power*game.gravity
                    elif game.gravity == -1:
                        self.y_speed = - power*game.gravity
            if 'l' in bouncy and last.right <= cell.left and\
                    self.collisionrect.right > cell.left:
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
                    self.collisionrect.left < cell.right:
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
        for cell in game.tilemap.layers["Triggers"].collide(self.collisionrect,
                                                            'deadly'):
            deadly = cell["deadly"]
            if 't' in deadly and last.bottom <= cell.top and\
                    self.collisionrect.bottom > cell.top:
                self.rect.bottom = cell.top
                self.respawn(game)
            if 'b' in deadly and last.top >= cell.bottom and\
                    self.collisionrect.top < cell.bottom:
                self.rect.top = cell.bottom
                self.respawn(game)
            if 'l' in deadly and last.right <= cell.left and\
                    self.collisionrect.right > cell.left:
                self.rect.right = cell.left
                self.respawn(game)
            if 'r' in deadly and last.left >= cell.right and\
                    self.collisionrect.left < cell.right:
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
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'Help'):
            helptext = cell['Help']
            if helptext != game.helpflagActive:
                game.helpflagActive = False
            if not game.getHelpFlag():
                game.helpflagActive = False
                game.currenthelp = helptext
                x, y = game.tilemap.pixel_from_screen(cell.px+cell.width/2,
                                                      cell.py-20)
                Help(x, y, game.sprites, game=game, Text=helptext)
        # ^--------------------------------------------------------------^
        # Test collision with exit trigger and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'playerExit'):
            level = cell["playerExit"]
            if game.mode not in ["singlemap"]:
                game.LoadLevel(level, game.campaignname,
                               game.mode, game.screen)
                game.loadLevelPart2(game.keys, self.soundslink)
            else:
                game.running = False
        # ^--------------------------------------------------------------^
        game.tilemap.set_focus(self.rect.x, self.rect.y)    # Sets screen focus
        # Wraps player movement if the glitch is active
        # v--------------------------------------------------------------v
        if game.glitches["hWrapping"]:
            # This piece of code should avoid phasing through the floor
            # v-----------------------------v
            if self.rect.x < 0:
                self.rect.x = game.tilemap.px_width - self.rect.width
                self.rect.y -= 3 * game.gravity
            elif self.rect.x > game.tilemap.px_width:
                self.rect.x = 0
                self.rect.y -= 3 * game.gravity
            # ^-----------------------------^
        # Handles the triggering of mobile platforms
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            "button"):
            if key[self.keys["action"]]:
                butt = cell['button']
                self.mod_logger.info("Player pressed the button \
                        with ID: %(butt)s" % locals())
                for plat in game.plats:
                    if plat.id == butt:
                        plat.active = True
                        plat.image = plat.activeimg
        # ^--------------------------------------------------------------^
        # Handles the triggering of teleporters
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            "TpIn"):
            if key[self.keys["action"]]:
                tpin = cell['TpIn']
                self.mod_logger.info("Player entered the TP with ID: %(tpin)s"
                                     % locals())
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
                self.collisionrect, 'CheckPoint'):
                chk = cell['CheckPoint']
                if chk == 1:
                    self.lastcheckpoint = (self.rect.x, self.rect.y)
                    cell['CheckPoint'] = 0
                    self.mod_logger.info("Checkpoint Saved")
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
        secondpass = [block for block in collision
                      if block.rect.colliderect(self.collisionrect)]
        for block in secondpass:
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
        self.animate(self.y_speed, self.x_speed, self.resting, self.bounced,
                     self.direction, dt, game.gravity, self.running,
                     self.pushing, self.glitched, game)
