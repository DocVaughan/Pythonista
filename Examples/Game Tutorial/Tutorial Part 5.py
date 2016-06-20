# coding: utf-8
'''
Part 5 -- Scores and Labels 💯

This part will be very simple, so you can relax a little -- you've come a long way already!

To show how many coins the player has collected, we're going to add a label that shows the current score. To use text in a scene, you can use a `LabelNode`, which is a simple subclass of `SpriteNode` that renders a string instead of an image.
'''

from scene import *
import sound
import random
A = Action

def cmp(a, b):
	return ((a > b) - (a < b))

standing_texture = Texture('plf:AlienGreen_front')
walk_textures = [Texture('plf:AlienGreen_walk1'), Texture('plf:AlienGreen_walk2')]

class Coin (SpriteNode):
	def __init__(self, **kwargs):
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
		# ---[1]
		# The font of a `LabelNode` is set using a tuple of font name and size.
		score_font = ('Futura', 40)
		self.score_label = LabelNode('0', score_font, parent=self)
		# The label is centered horizontally near the top of the screen:
		self.score_label.position = (self.size.w/2, self.size.h - 70)
		# The score should appear on top of everything else, so we set the `z_position` attribute here. The default `z_position` is 0.0, so using 1.0 is enough to make it appear on top of the other objects.
		self.score_label.z_position = 1
		self.score = 0
		self.walk_step = -1
		self.items = []
	
	def update(self):
		self.update_player()
		self.check_item_collisions()
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
		player_hitbox = Rect(self.player.position.x - 20, 32, 40, 65)
		for item in list(self.items):
			if item.frame.intersects(player_hitbox):
				self.collect_item(item)
			elif not item.parent:
				self.items.remove(item)
	
	def spawn_item(self):
		coin = Coin(parent=self)
		coin.position = (random.uniform(20, self.size.w-20), self.size.h + 30)
		d = random.uniform(2.0, 4.0)
		actions = [A.move_by(0, -(self.size.h + 60), d), A.remove()]
		coin.run_action(A.sequence(actions))
		self.items.append(coin)
		
	def collect_item(self, item, value=10):
		sound.play_effect('digital:PowerUp7')
		item.remove_from_parent()
		self.items.remove(item)
		# ---[2]
		# Simply add 10 points to the score for every coin, then update the score label accordingly:
		self.score += value
		self.score_label.text = str(self.score)

if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=True)