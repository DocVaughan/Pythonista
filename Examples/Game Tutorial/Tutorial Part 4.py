# coding: utf-8
'''
Part 4 -- Coins! 💰

Now that our alien can run around, let's add a bit of an incentive to do so... What could be a better motivation than gold raining from the sky?

As before, you'll find detailed explanations about the changes in this part directly in the code. Use the popup menu to navigate to the numbered sections.
'''

from scene import *
import sound
import random
A = Action

def cmp(a, b):
	return ((a > b) - (a < b))

standing_texture = Texture('plf:AlienGreen_front')
walk_textures = [Texture('plf:AlienGreen_walk1'), Texture('plf:AlienGreen_walk2')]

# ---[1]
# To represent the coins, we use a subclass of SpriteNode.
# This is not absolutely necessary (you could use plain SpriteNode objects as well), but it can be helpful if you have different kinds of items with unique attributes. For example, we might want to use different point values for different coins later.
class Coin (SpriteNode):
	def __init__(self, **kwargs):
		# Each coin uses the same built-in image/texture. The keyword arguments are simply passed on to the superclass's initializer, so that it's possible to pass a position, parent node etc. directly when initializing a Coin.
		SpriteNode.__init__(self, 'plf:Item_CoinGold', **kwargs)

class Game (Scene):
	def setup(self):
		self.background_color = '#004f82'
		self.ground = Node(parent=self)
		x = 0
		while x <= self.size.w + 64:
			tile = SpriteNode('plf:Ground_PlanetHalf_mid', position=(x, 0))
			self.ground.add_child(tile)
			x += 64
		self.player = SpriteNode(standing_texture)
		self.player.anchor_point = (0.5, 0)
		self.player.position = (self.size.w/2, 32)
		self.add_child(self.player)
		self.walk_step = -1
		# ---[2]
		# We need a new attribute to keep track of the coins that are in the game, so that we can check if any of them collides with the player:
		self.items = []
	
	def update(self):
		# ---[3]
		# To clean up the code a little, the player movement logic is now extracted to its own method.
		self.update_player()
		# This method checks for collisions between the player and all the coins:
		self.check_item_collisions()
		# In every frame, there's a 5% chance that a coin will appear at the top of the screen. Because `update()` is called 60 times per second, this corresponds to about 3 coins per second.
		if random.random() < 0.05:
			self.spawn_item()
	
	def update_player(self):
		g = gravity()
		if abs(g.x) > 0.05:
			self.player.x_scale = cmp(g.x, 0)
			x = self.player.position.x
			max_speed = 40
			x = max(0, min(self.size.w, x + g.x * max_speed))
			self.player.position = x, 32
			step = int(self.player.position.x / 40) % 2
			if step != self.walk_step:
				self.player.texture = walk_textures[step]
				sound.play_effect('rpg:Footstep00', 0.05, 1.0 + 0.5 * step)
				self.walk_step = step
		else:
			self.player.texture = standing_texture
			self.walk_step = -1
	
	def check_item_collisions(self):
		# ---[4]
		# To check if the player has collected a coin, we simply check for intersections between each of the coins' frames, and the player's hitbox. The hitbox is a bit smaller than the actual player sprite because some of its image is transparent.
		player_hitbox = Rect(self.player.position.x - 20, 32, 40, 65)
		# Note: We iterate over a copy of the items list (created using list(...)), so that we can remove items from it while iterating.
		for item in list(self.items):
			if item.frame.intersects(player_hitbox):
				self.collect_item(item)
			# When a coin has finished its animation, it is automatically removed from the scene by its Action sequence. When that's the case, also remove it from the `items` list, so it isn't checked for collisions anymore:
			elif not item.parent:
				self.items.remove(item)
	
	def spawn_item(self):
		# ---[5]
		# This gets called at random intervals from `update()` to create a new coin at the top of the screen.
		coin = Coin(parent=self)
		coin.position = (random.uniform(20, self.size.w-20), self.size.h + 30)
		# The coin's fall duration is randomly chosen somewhere between 2 and 4 seconds:
		d = random.uniform(2.0, 4.0)
		# To let the coin fall down, we use an `Action`.
		# Actions allow you to animate things without having to keep track of every frame of the animation yourself (as we did with the walking animation). Actions can be combined to groups and sequences. In this case, we create a sequence of moving the coin down, and then removing it from the scene.
		actions = [A.move_by(0, -(self.size.h + 60), d), A.remove()]
		coin.run_action(A.sequence(actions))
		# Also add the coin to the `items` list (used for checking collisions):
		self.items.append(coin)
		
	def collect_item(self, item):
		sound.play_effect('digital:PowerUp7')
		item.remove_from_parent()
		self.items.remove(item)

if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=True)