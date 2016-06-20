# coding: utf-8
'''
Part 1 -- Getting Started 🏁

Welcome to the game tutorial for Pythonista!

We're going to build a simple, motion-controlled game in easily-digestible steps. Each part of the tutorial builds upon the previous one, so be sure to read/try them in order.

In each step, we'll add new features to the game, introducing concepts of the `scene` module and some useful features of Pythonista IDE the along the way. You should have some experience with Python already, but you don't need to be an expert.

In the final game, you'll be able to control a little alien by tilting your device, while coins (good) and meteors (bad) rain from the sky...

So let's get started. We first need a subclass of `Scene` -- it's simply called `Game` here. This basically defines everything that happens on the screen -- the objects that are drawn, how touches are handled, etc.

The `Scene` class defines several methods that are intended to be overridden to customize its behavior. One of them is `setup`, which is called automatically just before the scene becomes visible on screen. This is a good place to set up the initial state of the game.

All visible objects in a game are represented by `Node`s, most often `SpriteNode`, which basically render an image. Nodes have a position, rotation, etc., and they can have "children", so you can modify a whole group of nodes as one.

We'll start by adding two nodes to the scene -- one representing the player (a green alien), and one for the ground he or she stands on. The ground is made of multiple tiles, but they're all added to one group `Node`, in case we want to easily move the entire ground elsewhere, without having to worry about the individual tiles.

The comments in the code below explain more details. Feel free to make your own changes, experiment with the values, and see what happens when you tap the run button (▶️).

Open the next part to learn how to make things move.
'''

from scene import *

class Game (Scene):
	def setup(self):
		# First, set a background color for the entire scene.
		# Tip: When you put the cursor inside the hex string, you can see a preview of the color directly in the editor. You can also tap the color swatch to select a new color visually.
		self.background_color = '#004f82'
		# Then create the ground node...
		# Usually, nodes are added to their parent using the `add_child()` method, but for convenience, you can also pass the node's parent as a keyword argument for the same effect.
		ground = Node(parent=self)
		x = 0
		# Increment x until we've reached the right edge of the screen...
		while x <= self.size.w + 64:
			tile = SpriteNode('plf:Ground_PlanetHalf_mid', position=(x, 0))
			ground.add_child(tile)
			# Each tile is 64 points wide.
			x += 64
		# Now create the player.
		# A SpriteNode can be initialized from a `Texture` object or simply the name of a built-in image, which we're using here.
		# Tip: When you put the cursor inside the name, you can see a small preview of the image -- you can also tap the preview image to select a different one.
		self.player = SpriteNode('plf:AlienGreen_front')
		# The `anchor_point` of a `SpriteNode` defines how its position/rotation is interpreted. By default, the position corresponds to the center of the sprite, but in this case, it's more convenient if the y coordinate corresponds to the bottom (feet) of the alien, so we can position it flush with the ground. The anchor point uses unit coordinates -- (0, 0) is the bottom-left corner, (1, 1) the top-right.
		self.player.anchor_point = (0.5, 0)
		# To center the player horizontally, we simply divide the width of the scene by two:
		self.player.position = (self.size.w/2, 32)
		self.add_child(self.player)

if __name__ == '__main__':
	# To actually get the scene on screen, you have to create an instance of your subclass (`Game`), and pass it to the `run()` function.
	# The `run()` function accepts a couple of different configuration arguments. In this case, we want the game to always run in portrait orientation, and we want to display a framerate counter. This can be useful during development -- if the framerate (fps) drops below 60 for an extended period of time, you'll probably want to start looking into performance optimizations.
	run(Game(), PORTRAIT, show_fps=True)