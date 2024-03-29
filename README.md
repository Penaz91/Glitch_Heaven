![](https://cloud.githubusercontent.com/assets/6682630/10658144/52151062-7894-11e5-8eaa-3bfb5f74cdc7.png)

![Status:Archived](https://img.shields.io/badge/Status-Archived-inactive)

Complete rewrite of my Glitch-Based Videogame that you can find in the
"The_Glitch" repository.

#### Official Presentation Website:
http://gh.penazarea.altervista.org

#### Status: Development

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
- **Bouncy Spikes glitch:** Deadly ground doesn't kill you, it makes you bounce twice as high (Can be applied from map editor by exchanging the "deadly" trigger with the "bouncy" trigger)
- **Deadly Bouncers Glitch:** Bouncers kill you (Can be applied from map editor by exchanging the "bouncy" trigger with the "deadly" trigger)
- **Invert-o-glitch**: Ground kills you, deadly ground doesn't. (Can be applied from map editor by exchanging the "deadly" trigger with the "blocker" trigger)
- **Non Working Bouncers:** Bouncers don't work (Can be applied from map editor by omitting the "bouncy" trigger)
- **Dead bodies Glitch:** when you die your dead body won't despawn and you can use it as a platform.
- **Clipping glitch**: You can glitch through certain walls (can be applied via map editor by omitting certain blocker parameters)
- **Solid Help Glitch**: The help text will behave like a temporary platform
- **Clip-on-command glitch**: Pressing down arrow makes you go through the platform you're standing on
- **LedgeJump Glitch:** If you walk out of a platform without jumping, you can jump in mid-air once while falling.
- **LedgeWalk Glitch:** if you go over a ledge, you don't fall. In order to fall you need to jump.
- **NoMovement Glitches:** A pack of 3 glitches (NoLeft, NoRight, NoJump) that disallow the usage of 1 or more commands for the player.
- **SlideInvert Glitch:** Pressing the action button (usually down arrow) will make the sliding floor pull you backwards.
- **StopBounce Glitch:** Pressing the action button (usually down arrow) will make you stop bouncing on the bouncy floor.
- **Speed Glitch:** Gotta go fast!!
- **Inverted Running:** You run by default, need to press the run button to walk
- **Inverted Controls:** Do i really have to explain this?
- **Invincibility Glitch:** you don't die to red floor.
- **Invincible to Obstacles Glitch** You don't die to mobile obstacles, meant as fix/addition to the Invincibility glitch. - Needs thorough testing
- **Movement toggle Glitch** You can't stop walking, you gotta keep moving!
- **TimeLapse glitch** Platforms and obstacles move only when you move horizontally
- **Intertia Glitches:** 2 glitches that will make the controls either very stiff or very slippery. Useful for very reaction-prone stages or to put the player in difficulty
- **Screen Wrap Glitch:** Going over the screen edge makes you wrap at the other end (Separated in horizontal and vertical Wrap)


### Glitches Partially Implemented or that need BuxFixes/Testing:
- **Resistance to lasers:** This will allow the player to use lasers as platforms

### Glitches Planned:
None at the moment

### Planned Features
- Make all interactibles require a press of the action button
- Better Particle Engine
- Sound Effects
- Music
- Animations
- **real** graphics
- In-game help

### Other Implemented Features:
- Password Locks: Find the password to unlock a terminal, button or exit
- Custom Maps and Campaigns support
- Infinite Savegames (As many as your HD can handle)

### Other info:
This Game uses Renfred Harper's Python3 port of Richard Jones's TMX Library to load maps.
