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
# ------------------------------------------------
import pygame
import os
from components.deadbody import DeadBody
from components.help import Help
from libs import animation
from libs import particle


class Player(pygame.sprite.Sprite):
    """ Class representing the player """
    size = (32, 32)     # Might be removed in future+taken from img
    playermaxspeed = 200
    runmultiplier = 2
    playeraccel = 50

    def __init__(self, location, *groups, keys):
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
        self.jumpsound = pygame.mixer.Sound(os.path.join("resources",
                                                         "sounds",
                                                         "jump.wav"))
        self.image = pygame.image.load(
                    os.path.join("resources",
                                 "sprites",
                                 "player.png")).convert_alpha()
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.resting = False
        self.y_speed = 0
        self.x_speed = 0
        self.jump_speed = -500
        self.direction = 1      # 1=Right, -1=Left
        self.bounced = False    # Used to ignore input when bounced
        self.keys = keys
        self.walkanimation = animation.Animation()
        self.walkanimation.loadFromDir(os.path.join("resources",
                                                    "sprites",
                                                    "Player",
                                                    "Walking"))
        self.runanimation = animation.Animation()
        self.runanimation.loadFromDir(os.path.join("resources",
                                                   "sprites",
                                                   "Player",
                                                   "Running"))
        self.particles = pygame.sprite.Group()

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
        if game.glitches["permbodies"]:
            x, y = game.tilemap.pixel_from_screen(self.rect.x,
                                                  self.rect.y)
            body = DeadBody(x, y, game.sprites, game=game)
            game.deadbodies.add(body)
        # ^-----------------------------------------------------^
        self.kill()     # Kills the player sprite
        # Does a complete respawn of the player
        # v-----------------------------------------------------v
        start_cell = game.tilemap.layers['Triggers'].find('playerEntrance')[0]
        game.player = Player((start_cell.px, start_cell.py),
                             game.sprites, keys=self.keys)
        # ^-----------------------------------------------------^

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
            self.direction = -1
            if not self.bounced:
                if key[self.keys["run"]]:
                    self.image = pygame.transform.flip(
                                 self.runanimation.next(),
                                 True,
                                 False)
                    self.x_speed = max(-self.playermaxspeed * dt *
                                       self.runmultiplier,
                                       self.x_speed-self.playeraccel*dt *
                                       self.runmultiplier)
                    # Emits particles if the player is on a surface
                    # Strength is increased because of running
                    # TODO: Decrease boilerplate for particle emission
                    # v----------------------------------------------------v
                    if self.resting:
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x+32, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), 2, -1, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x+32, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), 2, -2, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x+32, self.rect.y+32),
                                (0, 81, 138),
                                (141, 200, 241), 4, -1, self.particles)
                    # ^----------------------------------------------------^
                else:
                    self.image = pygame.transform.flip(
                                 self.walkanimation.next(),
                                 True,
                                 False)
                    self.x_speed = max(-self.playermaxspeed * dt,
                                       self.x_speed-self.playeraccel*dt)
                    # Emits particles if the player is on a surface
                    # TODO: Reduce Boilerplate for particle Emission
                    # v----------------------------------------------------v
                    if self.resting:
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x+32, self.rect.y+32), (0, 81, 138),
                            (141, 200, 241), 1, -1, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x+32, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), 1, -2, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x+32, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), 2, -1, self.particles)
                    # ^----------------------------------------------------^

        elif key[self.keys["right"]]:
            if not self.bounced:
                self.direction = 1
                if key[self.keys["run"]]:
                    self.image = self.runanimation.next()
                    self.x_speed = min(self.playermaxspeed * dt *
                                       self.runmultiplier,
                                       self.x_speed+self.playeraccel * dt *
                                       self.runmultiplier)
                    # Emits particles if the player is on a surface
                    # Strength is increased because of running
                    # TODO: Decrease boilerplate for particle emission
                    # v----------------------------------------------------v
                    if self.resting:
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x, self.rect.y+32), (0, 81, 138),
                            (141, 200, 241), -2, -1, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), -2, -2, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), -4, -1, self.particles)
                    # ^----------------------------------------------------^
                else:
                    self.image = self.walkanimation.next()
                    self.x_speed = min(self.playermaxspeed*dt,
                                       self.x_speed+self.playeraccel*dt)
                    # Emits particles if the player is on a surface
                    # Strength is increased because of running
                    # TODO: Decrease boilerplate for particle emission
                    # v----------------------------------------------------v
                    if self.resting:
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), -1, -1, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), -1, -2, self.particles)
                        particle.Particle(game.tilemap.pixel_to_screen(
                            self.rect.x, self.rect.y+32),
                            (0, 81, 138),
                            (141, 200, 241), -2, -1, self.particles)
                    # ^----------------------------------------------------^
        else:
            # Gives the player some control over the fall if they're not
            # bounced away from a spring
            # TODO: Find some better way to let player keep control
            # v--------------------------------------------------------------v
            if not self.bounced:
                if self.direction == 1:
                    self.x_speed = max(0, self.x_speed-(self.playeraccel*dt))
                elif self.direction == -1:
                    self.x_speed = min(0, self.x_speed+(self.playeraccel*dt))
            # ^--------------------------------------------------------------^
        self.rect.x += self.x_speed
        if game.glitches["multijump"]:
            if key[self.keys["jump"]]:
                self.jumpsound.play()
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    # If the high jump glitch is active, jumps twice as high
                    # This happens while the multijump glitch is active
                    # v------------------------------------------------------v
                    # TODO: Invert Comparations to save on CPU power
                    # if self.y_speed.....
                    #     if game.glitches ......
                    if game.glitches["highjump"]:
                        if self.y_speed > -(self.jump_speed/2) or self.resting:
                            self.y_speed = self.jump_speed*2*game.gravity
                    else:
                        if self.y_speed > -(self.jump_speed/2) or self.resting:
                            self.y_speed = self.jump_speed*game.gravity
                    # ^------------------------------------------------------^
        elif game.glitches["hover"]:
            if key[self.keys["jump"]]:
                self.jumpsound.play()
                self.y_speed = self.jump_speed*game.gravity*0.8
        else:
            if key[self.keys["jump"]] and self.resting:
                self.jumpsound.play()
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    if game.glitches["highjump"]:
                        self.y_speed = self.jump_speed*2*game.gravity
                    else:
                        self.y_speed = self.jump_speed*game.gravity
                    self.resting = False
        if game.glitches["featherfalling"]:
            if game.gravity == 1:
                self.y_speed = (min(200, self.y_speed+20))
            elif game.gravity == -1:
                self.y_speed = -(min(200, abs(self.y_speed)+20))
            # Why? Gravity will never be 0.
            # TODO: Find a reason for this useless piece of code or go
            # Order 66 on it
            elif game.gravity == 0:
                self.y_speed = 0
        else:
            if game.gravity == 1:
                self.y_speed = (min(400, self.y_speed+40))
            elif game.gravity == -1:
                self.y_speed = (max(-400, self.y_speed-40))
            # Why? Gravity will never be 0.
            # TODO: Find a reason for this useless piece of code or go
            # Order 66 on it
            elif game.gravity == 0:
                self.y_speed = 0
        self.rect.y += self.y_speed * dt
        self.resting = False
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
                        if game.gravity == -1:
                            self.resting = True
                else:
                    self.rect.top = cell.bottom
                    if game.glitches["stickyceil"]:
                        self.y_speed = -5/dt
                    else:
                        self.y_speed = 0
                    if game.gravity == -1:
                        self.resting = True
        for cell in game.tilemap.layers["Triggers"].collide(self.rect,
                                                            'bouncy'):
            bouncy = cell["bouncy"]
            power = int(cell["power"])
            if 't' in bouncy and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.rect.bottom = cell.top
                if game.gravity == 1:
                    self.y_speed = - power*game.gravity
                elif game.gravity == -1:
                    self.y_speed = power*game.gravity
            if 'b' in bouncy and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.rect.top = cell.bottom
                if game.gravity == 1:
                    self.y_speed = power*game.gravity
                elif game.gravity == -1:
                    self.y_speed = - power*game.gravity
            if 'l' in bouncy and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.bounced = True
                self.rect.right = cell.left
                self.x_speed = -power*dt
                if self.y_speed < 0:
                    self.y_speed = - game.gravity*power
                else:
                    self.y_speed = game.gravity*power
            if 'r' in bouncy and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.bounced = True
                self.rect.left = cell.right
                self.x_speed = power*dt
                if self.y_speed < 0:
                    self.y_speed = - game.gravity*power
                else:
                    self.y_speed = game.gravity*power
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
        collision = pygame.sprite.spritecollide(self, game.deadbodies, False)
        for block in collision:
            if self.y_speed == 0:
                self.resting = True
            elif self.y_speed > 0:
                self.rect.bottom = block.rect.top
                self.resting = True
                self.y_speed = 0
            elif self.y_speed < 0:
                self.rect.top = block.rect.bottom
                self.resting = False
                self.y_speed = 0
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
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'playerExit'):
            game.eraseCurrentLevel()
            game.loadNextLevel(game.currentcampaign, game.screen)
            game.loadLevelPart2(game.keys)
        game.tilemap.set_focus(self.rect.x, self.rect.y)
        game.backpos[0] = -game.tilemap.view_x
        if game.glitches["vwrapping"]:
            self.rect.y = self.rect.y % game.tilemap.px_height
        if game.glitches["hwrapping"]:
            self.rect.x = self.rect.x % game.tilemap.px_width
        else:
            if self.rect.y < 0 or self.rect.y > game.tilemap.px_height:
                self.respawn(game)
