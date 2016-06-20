# coding: utf-8

'''
A noise shader that produces an animation that looks a bit like bubbling lava... You can scroll infinitely in all directions via touch.
'''

from scene import *

class NoiseScene (Scene):
	def setup(self):
		with open('SimplexNoise.fsh') as f:
			src = f.read()
			shader = Shader(src)
		self.sprite = SpriteNode('SimplexNoiseGradient.png', size=self.size, position=self.size/2, parent=self)
		self.sprite.shader = shader
		self.offset = Vector2(0, 0)
		self.touch_start = Point(0, 0)
		
	def did_change_size(self):
		self.sprite.position = self.size/2
		self.sprite.size = self.size
	
	def touch_began(self, touch):
		self.touch_start = touch.location
	
	def touch_moved(self, touch):
		offset = self.offset + (self.touch_start - touch.location)
		self.sprite.shader.set_uniform('u_offset', offset)
	
	def touch_ended(self, touch):
		self.offset += (self.touch_start - touch.location)
		
run(NoiseScene(), multi_touch=False)