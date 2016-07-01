# Player component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from os.path import join as pjoin
import json
from components.deadbody import DeadBody
from components.help import Help
from components.UI.textinput import textInput
from libs.spritesheetanimation import SpritesheetAnimation as SpriteAni
from libs import emitter


class Player(pygame.sprite.Sprite):
    """ Class representing the player """
    _runpower_ = 2
    _jump_speed_ = -650
    _initialParticleColor_ = (0, 255, 84)
    _finalParticleColor_ = (0, 103, 34)
    _hovermodifier_ = 0.8

    def RealignCollision(self, gravity):
        """ re-aligns the drawing rect to the collision rect
        Parameter: The game gravity"""
        if gravity == 1:
            self.collisionrect.midbottom = self.rect.midbottom
        else:
            self.collisionrect.midtop = self.rect.midtop

    def fixCollision(self, gravity):
        if gravity == 1:
            self.rect.midbottom = self.collisionrect.midbottom
        else:
            self.rect.midtop = self.collisionrect.midtop

    def FeatherFallOn(self):
        """Turns on the featherfalling glitch"""
        self.maxFallSpeed = 350
        self.fallAccel = 35

    def FeatherFallOff(self):
        """Turns off the featherfalling glitch"""
        self.maxFallSpeed = 600
        self.fallAccel = 60

    def DoubleSpeedOn(self):
        """Turns on the Double Speed Glitch"""
        self.playermaxspeed = 350
        self.playeraccel = 100

    def DoubleSpeedOff(self):
        """Turns off the Double Speed Glitch"""
        self.playermaxspeed = 250
        self.playeraccel = 50

    def HiJumpOn(self):
        """Turns on the High Jump Glitch"""
        self.jumpMultiplier = 2

    def HiJumpOff(self):
        """Turns on the High Jump Glitch"""
        self.jumpMultiplier = 1

    def LowAccel(self):
        """Turns on the Low Acceleration Glitch"""
        self.playeraccel = 15

    def HighAccel(self):
        """Turns on the High Acceleration Glitch"""
        self.playeraccel = 100

    def ResetAccel(self):
        """Resets Acceleation glitches"""
        self.playeraccel = 50

    def loadSprites(self):
        """Loads sprites and animations, uses a JSON to generate paths quickly
        using a simple loop"""
        self.normalSprite = {
            "idle": None,
            "walk": None,
            "run": None,
            "bounced": None,
            "jump_rise": None,
            "jump_fall": None,
            "push": None
        }
        self.glitchedSprite = self.normalSprite.copy()
        self.generators = None
        with open(pjoin("resources", "datastructures",
                        "PlayerAniGen.json")) as gen:
            self.generators = json.loads(gen.read())
        for item in self.generators.keys():
            if self.generators[item]["is_Animation"]:
                self.normalSprite[item] = SpriteAni(self.generators[item]
                                                    ["frametime"],
                                                    pjoin("resources",
                                                          "sprites",
                                                          "Player",
                                                          item + ".png"))
                self.glitchedSprite[item] = SpriteAni(self.generators[item]
                                                      ["frametime"],
                                                      pjoin("resources",
                                                            "sprites",
                                                            "Glitched_Player",
                                                            item + ".png"))
            else:
                self.normalSprite[item] = pygame.image.load(
                        pjoin("resources", "sprites", "Player",
                              item + ".png")).convert_alpha()
                self.glitchedSprite[item] = pygame.image.load(
                        pjoin("resources", "sprites", "Glitched_Player",
                              item + ".png")).convert_alpha()

    def setupEmitters(self):
        """ Prepares the particle emitters"""
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
        """ Emits a spray of particles from the right emitter"""
        if self.game.gravity == 1:
            self.rightemitter.move(self.rect.bottomright)
        else:
            self.rightemitter.move(self.rect.topright)
        self.rightemitter.emit(self.runmultiplier,
                               self.runmultiplier*self.game.gravity)

    def emit_Left(self):
        """ Emits a spray of particles from the left emitter"""
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
        self.playeraccel = 30
        self.runmultiplier = 1
        self.jumpMultiplier = 1
        self.soundslink = sounds
        self.jumpsound = sounds["sfx"]["jump"]
        self.deathsound = sounds["sfx"]["death"]
        self.bouncesound = sounds["sfx"]["bounce"]
        self.loadSprites()
        self.image = self.normalSprite["idle"].currentframe
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.x, self.rect.y = location
        self.x_speed, self.y_speed = 0, 0
        self.direction = 1      # 1=Right, -1=Left
        self.keys = keys
        self.particles = pygame.sprite.Group()
        self.game = game
        if self.game.config["Video"]["playerparticles"]:
            self.setupEmitters()
        self.lastcheckpoint = location
        self.collisionrect = pygame.rect.Rect((0, 0), (20, 30))
        self.collisionrect.midbottom = self.rect.midbottom
        self.status = {
                "glitched": False,
                "resting": False,
                "bounced": False,
                "running": False,
                "pushing": False
                }

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
        x, y = game.tilemap.pixel_from_screen(self.rect.x,
                                              self.rect.y)

        self.mod_logger.info("Player respawned, death coords: (%(x)s, %(y)s)"
                             % locals())
        if game.glitches["permBodies"]:
            body = DeadBody(x, y, game.sprites, game=game)
            game.deadbodies.add(body)
        else:
            game.gameStatus["deathCounter"] += 1
        if game.glitches["invertedGravity"]:
            game.gravity = -1
        else:
            game.gravity = 1
        self.deathsound.play()
        # ^-----------------------------------------------------^
        # Does a complete respawn of the player
        # v-----------------------------------------------------v
        self.rect.x, self.rect.y = self.lastcheckpoint
        self.x_speed, self.y_speed = 0, 0
        self.RealignCollision(game.gravity)
        # game.player.rect.x, game.player.rect.y = self.lastcheckpoint
        # game.player.x_speed, game.player.y_speed = 0, 0
        # ^-----------------------------------------------------^

    def animate(self, yspeed, xspeed, resting, bounced,
                direction, dt, gravity, running, pushing, glitched, game):
        """ Takes care of the animation of the player entity, according to a set of
        properties of the player itself"""
        spriteList = None
        if glitched:
            spriteList = self.glitchedSprite
        else:
            spriteList = self.normalSprite
        if resting:
            # IDLE - Walk - Run code
            if xspeed == 0:
                # Player is idle
                if pushing:
                    self.image = spriteList["push"]
                else:
                    self.image = spriteList["idle"].next(dt)
            else:
                if running:
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
            elif yspeed * gravity <= 0:
                self.image = spriteList["jump_rise"]
        # Image Flipping
        self.image = pygame.transform.flip(self.image, (direction == -1),
                                           (gravity == -1))
        if game.gameStatus["modifiers"]["moonwalk"]:
            self.image = pygame.transform.flip(
                         self.image, True, False)
        # Particle emission
        if self.game.config["Video"]["playerparticles"]:
            if(xspeed != 0 and resting):
                if direction == 1:
                    self.emit_Left()
                else:
                    self.emit_Right()

    def emitJumpParticles(self):
        """ Emits a spray of particles from the both emitters"""
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
        # self.fixCollision(game.gravity)
        last = self.collisionrect.copy()  # Copy last position for compare
        key = pygame.key.get_pressed()
        # Check if run button is pressed (With eventual Invertedrun glitch)
        # v--------------------------------------------------------------v
        if game.glitches["invertedRun"]:
            self.status["running"] = not bool(key[self.keys["run"]])
        else:
            self.status["running"] = bool(key[self.keys["run"]])
        # ^--------------------------------------------------------------^
        if self.status["running"]:
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
            if not self.status["bounced"]:  # Not bounced away->control in air
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
            if not self.status["bounced"]:
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
                if not self.status["bounced"]:
                    if self.direction == 1:
                        self.x_speed = max(0,
                                           self.x_speed-(self.playeraccel*dt))
                    elif self.direction == -1:
                        self.x_speed = min(0,
                                           self.x_speed+(self.playeraccel*dt))
            # ^--------------------------------------------------------------^
        self.rect.x += self.x_speed         # Move the player
        # self.fixCollision(game.gravity)
        if game.glitches["multiJump"]:
            if key[self.keys["jump"]] and not game.glitches["noJump"]:
                # Plays the jump sound only with a player descending, to avoid
                # a sound spam
                if self.y_speed*game.gravity >= 0:
                    self.jumpsound.play()
                # In case of "gravity glitch", inverts gravity
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    # If the high jump glitch is active, jumps twice as high
                    # This happens while the multijump glitch is active
                    # v------------------------------------------------------v
                    if self.y_speed*game.gravity > -(self._jump_speed_/2) or\
                            self.status["resting"]:
                        self.y_speed = self._jump_speed_ * \
                           self.jumpMultiplier * game.gravity
                        if game.config["Video"]["playerparticles"]:
                            self.emitJumpParticles()
                    # ^------------------------------------------------------^
        elif game.glitches["hover"]:
            if key[self.keys["jump"]] and not game.glitches["noJump"]:
                # Makes the player fly in case of the hover glitch
                # v------------------------------------------------------v
                if self.status["resting"]:
                    self.jumpsound.play()
                self.y_speed = self._jump_speed_\
                    * game.gravity*self._hovermodifier_
                if game.config["Video"]["playerparticles"]:
                    self.emitJumpParticles()
                # ^------------------------------------------------------^
        else:
            if key[self.keys["jump"]] and self.status["resting"] and\
                    not game.glitches["noJump"]:
                # Takes care of the jumping, or gravity inversion
                self.jumpsound.play()
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    # If the high jump glitch is active, jumps twice as high
                    # v------------------------------------------------------v
                    self.y_speed = self._jump_speed_ * \
                            self.jumpMultiplier * game.gravity
                    if game.config["Video"]["playerparticles"]:
                        self.emitJumpParticles()
                    # ^------------------------------------------------------^
                    self.status["resting"] = False  # I jumped->not on surface
        # Takes care of the gravity and falling
        # v------------------------------------------------------v
        if game.gravity == 1:
            self.y_speed = min(self.maxFallSpeed,
                               self.y_speed + self.fallAccel)
        else:
            self.y_speed = max(-self.maxFallSpeed,
                               self.y_speed - self.fallAccel)
        # ^------------------------------------------------------^
        # Takes care of player movement and ledgewalk glitch
        # v------------------------------------------------------v
        if game.glitches['ledgeWalk']:
            if not self.status["resting"]:
                self.rect.y += self.y_speed * dt   # Move the player vertically
        else:
            self.rect.y += self.y_speed * dt    # Move the player vertically
        # ^------------------------------------------------------^
        self.RealignCollision(game.gravity)
        # This avoids the ability to jump in air after leaving a platform
        # + ledgejump glitch framework
        # v--------------v
        if not game.glitches["ledgeJump"] and not game.glitches["ledgeWalk"]:
            self.status["resting"] = False
        # ^--------------^
        # Test for collision with scrolling ground
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'slide'):
            top = last.bottom <= cell.top and\
                  self.collisionrect.bottom > cell.top
            bottom = last.top >= cell.bottom and\
                self.collisionrect.top < cell.bottom
            if (game.gravity == 1 and top) or\
               (game.gravity == -1 and bottom):
                slide = int(cell['slide'])
                if game.glitches["slideInvert"]:
                    if key[self.keys["action"]]:
                        slide *= -1
                self.collisionrect.x += slide * dt
                self.fixCollision(game.gravity)
        # ^--------------------------------------------------------------^
        # Test for collision with deadbody platforms and act accordingly
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.deadbodies, False)
        for block in collision:
            if game.gravity == 1:
                if last.bottom <= block.rect.top and\
                        self.collisionrect.bottom > block.rect.top:
                    self.rect.bottom = block.rect.top
            else:
                if last.top >= block.rect.bottom and\
                        self.collisionrect.top < block.rect.bottom:
                    self.rect.top = block.rect.bottom
            self.status["resting"] = True
            self.y_speed = 0
        # ^--------------------------------------------------------------^
        # Moving plats collision check
        # NOTE: This has to stay here to avoid being tped under a platform
        #       if you touch a vertical wall
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.plats, False)
        for block in collision:
            if block.active:
                top = last.bottom <= block.last.top and\
                    self.collisionrect.bottom > block.rect.top
                bottom = last.top >= block.last.bottom and\
                    self.collisionrect.top < block.rect.bottom
                if top or bottom:
                    if top:
                        self.collisionrect.bottom = block.rect.top
                    elif bottom:
                        self.collisionrect.top = block.rect.bottom
                    if block.bouncy:
                        self.y_speed = - block.bouncepwr * game.gravity
                        self.bouncesound.play()
                    else:
                        self.y_speed = block.yspeed * game.gravity
                        if (game.gravity == 1 and top) or\
                                (game.gravity == -1 and bottom):
                            self.status["resting"] = True
                if block.moving:
                    self.collisionrect.x += block.xspeed * dt * block.direction
            self.fixCollision(game.gravity)
        # self.collisionrect.midbottom = self.rect.midbottom
        # Test for collision with solid surfaces and act accordingly
        # v--------------------------------------------------------------v
        self.status["pushing"] = False
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'blocker'):
            blockers = cell['blocker']
            if 't' in blockers and last.bottom <= cell.top and\
                    self.collisionrect.bottom > cell.top:
                self.status["bounced"] = False
                # Corrects position only if you're not clipping via glitch
                # v----------------------------------------------------v
                if game.glitches["clipOnCommand"]:
                    if not key[self.keys["action"]]:
                        self.collisionrect.bottom = cell.top
                else:
                    self.collisionrect.bottom = cell.top
                # ^----------------------------------------------------^
                # Puts resting status if feet are colliding, else looks for a
                # stickyceil glitch and acts as a consequence
                # v----------------------------------------------------v
                if game.gravity == 1:
                    self.status["resting"] = True
                    self.y_speed = 0
                else:
                    if game.glitches["stickyCeil"] and\
                            not key[self.keys["action"]]:
                        self.y_speed = 5/dt
                    else:
                        self.y_speed = 0
                # ^----------------------------------------------------^
            elif 'b' in blockers and last.top >= cell.bottom and\
                    self.collisionrect.top < cell.bottom:
                # Part of the clip-on-command glitch Framework
                self.status["bounced"] = False
                # Corrects position only if you're not clipping via glitch
                # v----------------------------------------------------v
                if game.glitches["clipOnCommand"]:
                    if not key[self.keys["action"]]:
                        self.collisionrect.top = cell.bottom
                else:
                    self.collisionrect.top = cell.bottom
                # ^----------------------------------------------------^
                # Puts resting status if feet are colliding, else looks for a
                # stickyceil glitch and acts as a consequence
                # v----------------------------------------------------v
                if game.gravity == -1:
                    self.status["resting"] = True
                    self.y_speed = 0
                else:
                    if game.glitches["stickyCeil"] and\
                            not key[self.keys["action"]]:
                        self.y_speed = -5/dt
                    else:
                        self.y_speed = 0
                # ^----------------------------------------------------^
            elif 'l' in blockers and last.right <= cell.left and\
                    self.collisionrect.right > cell.left:
                self.status["bounced"] = False
                self.collisionrect.right = cell.left
                self.status["pushing"] = True
                self.x_speed = 0
                if game.glitches["wallClimb"]:
                        self.y_speed = -200 * game.gravity
            elif 'r' in blockers and last.left >= cell.right and\
                    self.collisionrect.left < cell.right:
                self.status["bounced"] = False
                self.collisionrect.left = cell.right
                self.status["pushing"] = True
                self.x_speed = 0
                if game.glitches["wallClimb"]:
                        self.y_speed = -200 * game.gravity
            self.fixCollision(game.gravity)
        # ^--------------------------------------------------------------^
        # Test for collision with bouncy platforms and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers["Triggers"].collide(self.collisionrect,
                                                            'bouncy'):
            bouncy = cell["bouncy"]
            power = int(cell["power"])
            if 't' in bouncy and last.bottom <= cell.top and\
                    self.collisionrect.bottom > cell.top:
                self.collisionrect.bottom = cell.top
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    self.y_speed = - power
            if 'b' in bouncy and last.top >= cell.bottom and\
                    self.collisionrect.top < cell.bottom:
                self.collisionrect.top = cell.bottom
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    self.y_speed = power
            if 'l' in bouncy and last.right <= cell.left and\
                    self.collisionrect.right > cell.left:
                self.collisionrect.right = cell.left
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    self.status["bounced"] = True
                    self.x_speed = -power*dt
                    directioner = -1 if (self.y_speed <= 0) else 1
                    self.y_speed = game.gravity*power*directioner
            if 'r' in bouncy and last.left >= cell.right and\
                    self.collisionrect.left < cell.right:
                self.collisionrect.left = cell.right
                if not (key[self.keys["action"]] and
                        game.glitches["stopBounce"]):
                    self.bouncesound.play()
                    self.status["bounced"] = True
                    self.x_speed = power*dt
                    directioner = -1 if (self.y_speed <= 0) else 1
                    self.y_speed = game.gravity*power*directioner
            self.fixCollision(game.gravity)
        # ^--------------------------------------------------------------^
        # Test for collisions with deadly ground and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers["Triggers"].collide(self.collisionrect,
                                                            'deadly'):
            deadly = cell["deadly"]
            if 't' in deadly and last.bottom <= cell.top and\
                    self.collisionrect.bottom > cell.top:
                self.rect.bottom = cell.top
            if 'b' in deadly and last.top >= cell.bottom and\
                    self.collisionrect.top < cell.bottom:
                self.rect.top = cell.bottom
            if 'l' in deadly and last.right <= cell.left and\
                    self.collisionrect.right > cell.left:
                self.rect.right = cell.left
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
                    self.status["resting"] = True
                elif self.y_speed > 0 and game.gravity == 1:
                    self.rect.bottom = block.rect.top
                    self.status["resting"] = True
                    self.y_speed = 0
                elif self.y_speed < 0 and game.gravity == -1:
                    self.rect.top = block.rect.bottom
                    self.status["resting"] = False
                    self.y_speed = 0
        # ^--------------------------------------------------------------^
        # Test collision with help triggers and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'Help'):
            if key[self.keys["action"]]:
                if "password" in cell:
                    pw = cell["password"]
                else:
                    pw = None
                passed = False
                if pw:
                    guess = textInput(game.screen, game.font,
                                      "Password required").get_input()
                    if guess == pw:
                        passed = True
                else:
                    passed = True
                if passed:
                    helptext = cell['Help']
                    if helptext != game.currenthelp:
                        game.helpflagActive = False
                    if not game.helpflagActive:
                        game.helpflagActive = False
                        game.currenthelp = helptext
                        x, y = game.tilemap.pixel_from_screen(
                                cell.px+cell.width/2,
                                cell.py-20)
                        Help(x, y, game.sprites, game=game, Text=helptext)
        # ^--------------------------------------------------------------^
        # Test collision with exit trigger and act accordingly
        # v--------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            'playerExit'):
            if key[self.keys["action"]]:
                level = cell["playerExit"]
                if "password" in cell:
                    pw = cell["password"]
                else:
                    pw = None
                passed = False
                if pw:
                    guess = textInput(game.screen, game.font,
                                      "Password required").get_input()
                    if guess == pw:
                        passed = True
                else:
                    passed = True
                if passed:
                    if game.gameStatus["mode"] not in ["singlemap"]:
                        game.LoadLevel(level, game.gameStatus["campaignName"],
                                       game.gameStatus["mode"], game.screen)
                        if level:
                            game.loadLevelPart2(game.keys, self.soundslink)
                    else:
                        game.running = False
        # ^--------------------------------------------------------------^
        game.tilemap.set_focus(self.rect.x, self.rect.y)    # Sets screen focus
        # Wraps player movement if the glitch is active
        # v--------------------------------------------------------------v
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
        """for cell in game.tilemap.layers['Triggers'].collide(self.collisionrect,
                                                            "button"):
            if key[self.keys["action"]]:
                butt = cell['button']
                if "password" in cell:
                    pw = cell["password"]
                else:
                    pw = None
                passed = False
                if pw:
                    guess = textInput(game.screen, game.font,
                                      "Password required").get_input()
                    if guess == pw:
                        passed = True
                else:
                    passed = True
                if passed:
                    for plat in game.plats:
                        if plat.id == butt:
                            plat.active = True
                            plat.image = plat.activeimg
                            self.mod_logger.info("Player pressed the button \
                                    with ID: %(butt)s" % locals())"""
        if key[self.keys["action"]]:
            for item in pygame.sprite.spritecollide(self, game.btns,
                                                    False):
                passed = False
                if item.password:
                    guess = textInput(game.screen, game.font,
                                      "Password required").get_input()
                    if guess == item.password:
                        passed = True
                else:
                    passed = True
                if passed:
                    for plat in game.plats:
                        if plat.id == item.id:
                            plat.active = True
                            plat.image = plat.activeimg
                            item.activate()
                            self.mod_logger.info("Player pressed the button \
                                    with ID: {0}".format(item.id))
            # Checkpoint Handling
            for item in pygame.sprite.spritecollide(self, game.checkpoints,
                                                    False):
                if not item.used:
                    self.lastcheckpoint = (self.rect.x, self.rect.y)
                    item.activate()
                    self.mod_logger.info("Checkpoint Saved")
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
                        self.collisionrect.x = out.px
                        self.collisionrect.y = out.py
                        self.fixCollision(game.gravity)
        # ^--------------------------------------------------------------^
        # Handles the Glitched Area animations
        # v--------------------------------------------------------------v
        self.status["glitched"] = False
        if game.tilemap.layers['Triggers'].collide(
                self.rect, "GlitchedAnimation") != []:
            self.status["glitched"] = True
        # ^--------------------------------------------------------------^
        # Handles The checkpoints
        # v--------------------------------------------------------------v
        """for cell in game.tilemap.layers['Triggers'].collide(
                self.collisionrect, 'CheckPoint'):
                chk = cell['CheckPoint']
                if chk == 1:
                    self.lastcheckpoint = (self.rect.x, self.rect.y)
                    cell['CheckPoint'] = 0
                    self.mod_logger.info("Checkpoint Saved")"""
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
        if game.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
            redcoll = game.tilemap.pixel_to_screen(self.rect.x, self.rect.y)
            self.status["glitched"] = redcoll[1] < game.redsurfrect.bottom
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
                        self.status["resting"] = True  # Allows jump
                    elif game.gravity == -1 and\
                            self.rect.top < block.rect.bottom:
                        self.rect.top = block.rect.bottom
                        self.y_speed = - block.yspeed
                        self.status["resting"] = True  # Allows jump
                self.rect.x += block.xspeed * dt * block.direction
            else:
                self.respawn(game)
        # Handles touching lasers
        # v--------------------------------------------------------------v
        collision = pygame.sprite.spritecollide(self, game.lasers, False)
        secondpass = [laser for laser in collision if laser.active]
        for block in secondpass:
            if game.glitches["laserresistant"]:
                # FIXME: Screen trembles when on lasers
                # FIXME: Need to make vertical lasers work like walls
                if self.y_speed * game.gravity >= 0:
                    if game.gravity == 1 and self.rect.bottom > block.rect.top:
                        self.rect.bottom = block.rect.top
                        self.status["resting"] = True  # Allows jump
                    elif game.gravity == -1 and\
                            self.rect.top < block.rect.bottom:
                        self.rect.top = block.rect.bottom
                        self.status["resting"] = True  # Allows jump
            else:
                self.respawn(game)
        # MUST BE LAST OPERATION
        # v--------------------------------------------------------------v
        self.animate(self.y_speed, self.x_speed, self.status["resting"],
                     self.status["bounced"],
                     self.direction, dt, game.gravity, self.status["running"],
                     self.status["pushing"], self.status["glitched"], game)
