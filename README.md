Vertical Scroll Shooter Documentation


Vertical Scroll Shooter is a game where the player controls a spaceship and fights enemy ships and obstacles. The aim of the game is to collect as many points as possible by destroying enemies and avoiding obstacles. The game ends when the player loses all lives or reaches a certain number of points.

Classes:

•	Player:
The Player class represents the player (the spaceship). It has the following attributes and methods:

o	image: the image of the player
o	rect: a rectangle describing the player's position on the screen
o	speed: player speed
o	radius: radius of the player
o	update(keys): method that updates the player's position depending on the keys pressed

•	PlayerHealth:
The PlayerHealth class represents the player's life. It has the following attributes and methods:

o	max_health: player's maximum number of lives
o	current_health: player's current health count
o	image: the image of the player's life
o	health_bar: the bar that shows the player's health level
o	rect: a rectangle describing the player's life position on the screen
o	health_bar_rect: a rectangle describing the position of the health bar on the screen
o	decrease_health(): method that decreases the player's health count
o	update(): a method that does nothing (for now)
o	draw(surface): method that draws the player's life on a given surface

•	Enemy:
The Enemy class represents the enemies in the game. They have the following attributes and methods:

o	image: the image of the enemy
o	rect: a rectangle describing the position of the enemy on the screen
o	speed: enemy speed
o	radius: enemy radius
o	shoot(): method that spawns bullets from the enemy
o	update(): a method that updates the enemy's position

•	Bullets:
The Bullet class represents the player's bullets. They have the following attributes and methods:

o	image: the image of the bullet
o	rect: a rectangle describing the position of the bullet on the screen
o	speed: bullet speed
o	update(): method that updates the position of the bullet

•	EnemyBullet:
The EnemyBullet class represents the enemy bullets. They have the following attributes and methods:

o	image: the image of the enemy bullet
o	rect: a rectangle describing the position of the bullet on the screen
o	seed: bullet speed
o	update(): method that updates the bullet's position and destroys it if it goes off the screen

•	Explosion:
The Explosion class represents the explosion animation. It has the following attributes and methods:

o	frame_index: the current frame index of the animation
o	image: the image of the current frame of the animation
o	rect: a rectangle describing the position of the animation on the screen
o	update(): method that updates the current frame of the animation

•	Main Game Loop:
In the main game loop, events are processed, game state is updated, and all sprites are drawn on the screen.
