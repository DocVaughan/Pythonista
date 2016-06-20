'''
A swarm simulation based on the 'Boids' algorithm by Craig Reynolds (http://www.red3d.com/cwr/boids/) and pseudo-code by Conrad Parker (http://www.kfish.org/boids/pseudocode.html)

You can tap the screen to scatter the swarm temporarily.
'''

from scene import *
import sound
from random import uniform, choice
import math
A = Action

SWARM_SIZE = 30
MAX_SPEED = 6

class Boid (SpriteNode):
	def __init__(self, max_x, max_y, *args, **kwargs):
		img = choice(['plf:Enemy_FishGreen', 'plf:Enemy_FishPink'])
		SpriteNode.__init__(self, img, *args, **kwargs)
		self.scale = 0.6
		self.max_x = max_x
		self.max_y = max_y
		a = uniform(0, math.pi*2)
		self.position = (uniform(0, max_x), uniform(0, max_y))
		self.v = Vector2(math.cos(a), math.sin(a))
		self.startled = False
	
	def update(self, neighbors):
		self.rule1(neighbors)
		self.rule2(neighbors)
		self.rule3(neighbors)
		self.rule4(neighbors)
		if abs(self.v) > MAX_SPEED:
			self.v *= (MAX_SPEED / abs(self.v))
		
	def rule1(self, neighbors):
		# Move to 'center of mass' of neighbors
		if not neighbors:
			return Vector2(0, 0)
		p = Point()
		for n in neighbors:
			p += n.position
		m = p / len(neighbors)
		if self.startled:
			self.v -= (m - self.position) * 0.007
		else:
			self.v += (m - self.position) * 0.001
	
	def rule2(self, neighbors):
		# Don't crowd neighbors
		if not neighbors:
			return Vector2(0, 0)
		c = Vector2()
		for n in neighbors:
			if abs(n.position - self.position) < 30:
				c += (self.position - n.position)
		self.v += c * 0.01
	
	def rule3(self, neighbors):
		# Match velocity of neighbors
		if not neighbors:
			return Vector2(0, 0)
		v = Vector2()
		for n in neighbors:
			v += n.v
		m = v / len(neighbors)
		self.v += m * 0.01
	
	def rule4(self, neighbors):
		# Stay within screen bounds
		v = Vector2()
		if self.position.x < 0:
			v.x = 1
		if self.position.x > self.max_x:
			v.x = -1
		if self.position.y < 0:
			v.y = 1
		if self.position.y > self.max_y:
			v.y = -1
		self.v += v * 0.3

class SwarmScene (Scene):
	def setup(self):
		self.swarm = [Boid(self.size.w, self.size.h, parent=self) for i in range(SWARM_SIZE)]
		self.background_color = '#003f67'
	
	def did_change_size(self):
		for b in self.swarm:
			b.max_x = self.size.w
			b.max_y = self.size.h
	
	def update(self):
		for boid in self.swarm:
			neighbor_distance = min(self.size)/3
			neighbors = [b for b in self.swarm if b != boid and abs(b.position - boid.position) < neighbor_distance]
			boid.update(neighbors)
		for boid in self.swarm:
			boid.position += boid.v
			boid.rotation = math.atan2(*reversed(boid.v)) + math.pi
	
	def touch_began(self, touch):
		self.panic(touch.location)
	
	def panic(self, pos):
		sound.play_effect('drums:Drums_06')
		for b in self.swarm:
			b.startled = True
		s = SpriteNode('shp:wavering', position=pos, scale=0, parent=self)
		s.run_action(A.sequence(A.group(A.scale_to(2), A.fade_to(0)), A.remove()))
		self.run_action(A.sequence(A.wait(1), A.call(self.end_panic)))
		
	def end_panic(self):
		for b in self.swarm:
			b.startled = False
			
if __name__ == '__main__':
	run(SwarmScene(), show_fps=True)