# coding: utf-8
'''
Part 2 -- Motion Control 👋

The scene we created in the previous part already started to look like the static screenshot of a game, but nothing was moving! So let's change that.

After implementing the `setup()` method, we now override a second one: `update()`. Unlike `setup()`, which gets called exactly once, this gets called *very* often, usually 60 times per second. This means that you have to be somewhat careful not to do too much in there. If the method takes longer than about the 60th of a second (~0.0167) to execute, you'll see stuttery animations.

To move the player left and right, we're going to use the device's accelerometer.

To jump straight to the `update` method, and see how this is done, tap the filename in the toolbar at the top. You'll get a list of all classes and methods that you can use to navigate quickly in long programs.
'''

from scene import *

class Game (Scene):
	def setup(self):
		self.background_color = '#004f82'
		ground = Node(parent=self)
		x = 0
		while x <= self.size.w + 64:
			tile = SpriteNode('plf:Ground_PlanetHalf_mid', position=(x, 0))
			ground.add_child(tile)
			x += 64
		self.player = SpriteNode('plf:AlienGreen_front')
		self.player.anchor_point = (0.5, 0)
		self.player.position = (self.size.w/2, 32)
		self.add_child(self.player)
	
	def update(self):
		# The gravity() function returns an (x, y, z) vector that describes the current orientation of your device. We only use the x component here, to steer left and right.
		g = gravity()
		if abs(g.x) > 0.05:
			x = self.player.position.x
			# The components of the gravity vector are in the range 0.0 to 1.0, so we have to multiply it with some factor to move the player more quickly. 40 works pretty well, but feel free to experiment. 
			max_speed = 40
			# We simply add the x component of the gravity vector to the current position, and clamp the value between 0 and the scene's width, so the alien doesn't move outside of the screen boundaries.
			x = max(0, min(self.size.w, x + g.x * max_speed))
			self.player.position = (x, 32)

if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=True)