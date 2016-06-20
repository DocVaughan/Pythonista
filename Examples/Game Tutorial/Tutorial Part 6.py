# coding: utf-8
'''
Part 6 -- Meteors Incoming! ☄️

Collecting coins is fun, but did you notice the distinct lack of... challenge?

Let's change that now, and add some meteors to the mix. The mechanism is essentially the same as with the coins, but when the alien collides with a meteor, the game is over.

To make the game a bit harder, the speed at which coins and meteors fall to the ground now increases slightly over time.
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
# Because the alien can be hit by a meteor, we need one additional texture for the unhappy alien:
hit_texture = Texture('plf:AlienGreen_hit')

class Coin (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'plf:Item_CoinGold', **kwargs)

# ---[2]
# As with the coins, we use a custom subclass of SpriteNode to represent the meteors. For some variety, the texture of the meteor is chosen randomly.
class Meteor (SpriteNode):
	def __init__(self, **kwargs):
		img = random.choice(['spc:MeteorBrownBig1', 'spc:MeteorBrownBig2'])
		SpriteNode.__init__(self, img, **kwargs)

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
		self.add_child(self.player)
		score_font = ('Futura', 40)
		self.score_label = LabelNode('0', score_font, parent=self)
		self.score_label.position = (self.size.w/2, self.size.h - 70)
		self.score_label.z_position = 1
		self.items = []
		# ---[3]
		# Because the game can end now, we need a method to restart it.
		# Some of the initialization logic that was previously in `setup()` is now in `new_game()`, so it can be repeated without having to close the game first.
		self.new_game()
	
	def new_game(self):
		# Reset everything to its initial state...
		for item in self.items:
			item.remove_from_parent()
		self.items = []
		self.score = 0
		self.score_label.text = '0'
		self.walk_step = -1
		self.player.position = (self.size.w/2, 32)
		self.player.texture = standing_texture
		self.speed = 1.0
		# ---[4]
		# The game_over attribute is set to True when the alien gets hit by a meteor. We use this to stop player movement and collision checking (the update method simply does nothing when game_over is True).
		self.game_over = False
	
	def update(self):
		if self.game_over:
			return
		self.update_player()
		self.check_item_collisions()
		if random.random() < 0.05 * self.speed:
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
		# ---[5]
		# The hit testing is essentially the same as before, but now distinguishes between coins and meteors (simply by checking the class of the item).
		# When a meteor hits, the game is over (see the `player_hit()` method below).
		player_hitbox = Rect(self.player.position.x - 20, 32, 40, 65)
		for item in list(self.items):
			if item.frame.intersects(player_hitbox):
				if isinstance(item, Coin):
					self.collect_item(item)
				elif isinstance(item, Meteor):
					self.player_hit()
			elif not item.parent:
				self.items.remove(item)
	
	def player_hit(self):
		# ---[6]
		# This is. alled from `check_item_collisions()` when the alien collides with a meteor. The alien simply drops off the screen, and after 2 seconds, a new game is started.
		self.game_over = True
		sound.play_effect('arcade:Explosion_1')
		self.player.texture = hit_texture
		self.player.run_action(A.move_by(0, -150))
		# Note: The duration of the `wait` action is multiplied by the current game speed, so that it always takes exactly 2 seconds, regardless of how fast the rest of the game is running.
		self.run_action(A.sequence(A.wait(2*self.speed), A.call(self.new_game)))
	
	def spawn_item(self):
		if random.random() < 0.3:
			# ---[7]
			# Whenever a new item is created, there's now a 30% chance that it is a meteor instead of a coin.
			# Their behavior is very similar to that of the coins, but instead of moving straight down, they may come in at an angle. To accomplish this, the x coordinate of the final position is simply chosen randomly.
			meteor = Meteor(parent=self)
			meteor.position = (random.uniform(20, self.size.w-20), self.size.h + 30)
			d = random.uniform(2.0, 4.0)
			actions = [A.move_to(random.uniform(0, self.size.w), -100, d), A.remove()]
			meteor.run_action(A.sequence(actions))
			self.items.append(meteor)
		else:
			coin = Coin(parent=self)
			coin.position = (random.uniform(20, self.size.w-20), self.size.h + 30)
			d = random.uniform(2.0, 4.0)
			actions = [A.move_by(0, -(self.size.h + 60), d), A.remove()]
			coin.run_action(A.sequence(actions))
			self.items.append(coin)
		# ---[8]
		# To make things a bit more interesting, the entire game gets slightly faster whenever a new item is spawned. The `speed` attribute is essentially a multiplier for the duration of all actions in the scene. Note that this is actually an attribute of `Node`, so you could apply different speeds for different groups of nodes. Since all items are added directly to the scene in this example, we don't make use of that here though.
		self.speed = min(3, self.speed + 0.005)
		
	def collect_item(self, item, value=10):
		sound.play_effect('digital:PowerUp7')
		item.remove_from_parent()
		self.items.remove(item)
		self.score += value
		self.score_label.text = str(self.score)

if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=True)