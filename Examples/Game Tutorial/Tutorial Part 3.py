# coding: utf-8
'''
Part 3 -- Walk Cycle and Sound Effects 🏃

In the previous part, our little alien moved left and right, but it all looked a bit unnatural. It might be different for aliens, but we usually don't just slide on the ground without moving our feet, while always looking in the same direction...

We're going to add a very simple walk cycle animation in this part -- and while we're at it, some footstep sounds too.

The changes in this part are numbered. You can navigate between them using the popup menu that appears when you tap the filename.
'''

from scene import *
import sound

def cmp(a, b):
	return ((a > b) - (a < b))

# ---[1]
# We need a few different textures for the player now, so it's best to load them just once. The walk cycle consists of two textures, and the previous texture is used when the alien is standing still.
standing_texture = Texture('plf:AlienGreen_front')
walk_textures = [Texture('plf:AlienGreen_walk1'), Texture('plf:AlienGreen_walk2')]

class Game (Scene):
	def setup(self):
		self.background_color = '#004f82'
		ground = Node(parent=self)
		x = 0
		while x <= self.size.w + 64:
			tile = SpriteNode('plf:Ground_PlanetHalf_mid', position=(x, 0))
			ground.add_child(tile)
			x += 64
		self.player = SpriteNode(standing_texture)
		self.player.anchor_point = (0.5, 0)
		self.player.position = (self.size.w/2, 32)
		self.add_child(self.player)
		# ---[2]
		# This attribute simply keeps track of the current step in the walk cycle. When the alien is standing still, it's set to -1, otherwise it changes between 0 and 1, corresponding to an index into the `walk_textures` list.
		self.walk_step = -1
	
	def update(self):
		g = gravity()
		if abs(g.x) > 0.05:
			#---[3]
			# The alien should look in the direction it's walking. By simply setting the `x_scale` attribute to -1 (when moving left) or 1 (when moving right), we only need one image for both directions. Setting the `x_scale` to a negative value has the effect of flipping the image horizontally.
			self.player.x_scale = cmp(g.x, 0)
			x = self.player.position.x
			max_speed = 40
			x = max(0, min(self.size.w, x + g.x * max_speed))
			self.player.position = x, 32
			# ---[4]
			# The current step in the walk cycle is simply derived from the current position. Every 40 points, the step changes from 0 to 1, and back again.
			step = int(self.player.position.x / 40) % 2
			if step != self.walk_step:
				# If the step has just changed, switch to a different texture...
				self.player.texture = walk_textures[step]
				# ...and play a 'footstep' sound effect.
				# The sound effect is always the same, but the pitch is modified by the current step, so it sounds like the two feet are making slightly different noises. The second parameter is the volume of the effect, which is set to a pretty low value here, so that the footsteps aren't too loud.
				sound.play_effect('rpg:Footstep00', 0.05, 1.0 + 0.5 * step)
				self.walk_step = step
		else:
			# If the alien is standing still (the device's tilt is below a certain threshold), use the 'standing' texture, and reset the walk cycle:
			self.player.texture = standing_texture
			self.walk_step = -1

if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=True)