# Glitch_Heaven
Complete rewrite of my Glitch-Based Videogame that you can find in the
"The_Glitch" repository.

#### Status: Prototyping

### Objective of the game
Get to the exit door of the level, using some hidden glitches that
have been volountarily inserted.
Further in the game, some glitches will make the user experience harder
and more challenging.

### Glitches Implemented:
- **Wall Climb Glitch:** if you collide with a wall and keep colliding, you'll find yourself climbing the wall
- **High Jump Glitch:** Each jump is twice as high
- **Feather Falling glitch:** You fall at half the normal speed
- **Gravity glitch:** instead of jumping you reverse gravity. (Incompatible with all jumping glitches)
- **Multiple jump Glitch:** you can jump countless times in the air.
- **Hovering glitch:** If you keep the jump button pressed you'll keep going up, like you were flying.
- **Inverted gravity:** EVERYTHING'S UPSIDE DOWN!!
- **Sticky Ceiling glitch:** if you jump and hit the ceiling, you'll stick there till you press "down arrow"
- **Invincibility Glitch:** you don't die to obstacles. (Can be applied from map editor by exchanging the "deadly" trigger with the "blocker" trigger)
- **Bouncy Spikes glitch:** Deadly ground doesn't kill you, it makes you bounce twice as high (Can be applied from map editor by exchanging the "deadly" trigger with the "bouncy" trigger)
- **Deadly Bouncers Glitch:** Bouncers kill you (Can be applied from map editor by exchanging the "bouncy" trigger with the "deadly" trigger)
- **Invert-o-glitch**: Ground kills you, deadly ground doesn't. (Can be applied from map editor by exchanging the "deadly" trigger with the "blocker" trigger)
- **Non Working Bouncers:** Bouncers don't work (Can be applied from map editor by exchanging the "deadly" trigger with the "bouncy" trigger)
- **Dead bodies Glitch:** when you die your dead body won't despawn and you can use it as a platform.
- **Clipping glitch**: You can glitch through certain walls (can be applied via map editor by omitting certain blocker parameters)


### Glitches Partially Implemented or that need BuxFixes/Testing:
None At The moment

### Glitches Planned:
- **Ledge Glitch:** if you go over a ledge, you don't fall. In order to fall you need to jump.
- **Clip-on-command glitch**: Pressing down arrow makes you go through the platform you're standing on
- **Solid Help Glitch**: The help text will behave like a temporary platform
- **Screen Wrap Glitch:** Going over the screen edge makes you wrap at the other end

### Other info:
This Game uses Renfred Harper's Python3 port of Richard Jones's TMX Library to load maps.
