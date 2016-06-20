# coding: utf-8

'''
An experimental hybrid of an analog and digital stopwatch -- tap anywhere to start/stop/reset.
'''

from scene import *
import sound
from functools import partial
from time import time
import ui

if min(ui.get_screen_size()) < 750:
	digit_h = 60
else:
	digit_h = 100
digit_w = digit_h * 0.9

invert_shader_src = '''
#extension GL_EXT_shader_framebuffer_fetch : require
void main() {gl_FragColor = vec4(1.0 - gl_LastFragData[0].rgb, 1.0);}
'''

class ReelNode (Node):
	def __init__(self, count=10):
		Node.__init__(self)
		self.count = count
		self.labels = []
		self.container = Node(parent=self)
		font = ('Avenir Next', digit_h)
		for i in range(count * 3):
			label = LabelNode(str(i%count), font=font)
			label.position = 0, -i * digit_h
			self.container.add_child(label)
			self.labels.append(label)
		self.set_value(0)
	
	def set_value(self, value):
		value = min(self.count, max(0, value))
		self.value = value
		y = self.count * digit_h + digit_h * value
		self.container.position = (0, y)
		for label in self.labels:
			label_y = y + label.position.y
			label.alpha = 1.0 - abs(label_y) / (digit_h*5.0)
			label.scale = label.alpha
	
	def animate_to(self, value, d=0.2):
		from_value = self.value
		to_value = value
		def anim(from_value, to_value, node, p):
			node.set_value(from_value + p * (to_value-from_value))
		animation = Action.call(partial(anim, from_value, to_value), d)
		self.run_action(animation)
		
class StopWatch (Scene):
	def setup(self):
		self.started = False
		self.start_time = 0
		self.stopped = False
		self.root = Node(parent=self)
		self.reels = []
		for i in range(5):
			reel = ReelNode(count=6 if i in (0, 2) else 10)
			x = (i-2) * digit_w
			x += 10 * (1 if i%2 == 0 else -1)
			reel.position = x, 0
			self.root.add_child(reel)
			self.reels.append(reel)
		colon = LabelNode(':', font=('Avenir Next', digit_h), position=(-digit_w/2, 0), parent=self.root)
		dot = LabelNode('.', font=('Avenir Next', digit_h), position=(digit_w*1.5, 0), parent=self.root)
		overlay = SpriteNode(size=(max(self.size), digit_h + 10))
		overlay.shader = Shader(invert_shader_src)
		self.root.add_child(overlay)
		self.background_color = 'black'
		self.did_change_size()
	
	def did_change_size(self):
		self.root.position = self.size/2
		
	def update(self):
		if not self.started:
			return
		elapsed = time() - self.start_time
		minutes = elapsed // 60
		seconds = elapsed % 60.0
		v4 = elapsed % 1.0 * 10.0
		v3 = seconds % 10
		v2 = (seconds // 10) + v3 / 10.0
		v1 = minutes % 10 + seconds / 60.0
		v0 = minutes // 10 + v1 / 10.0
		self.reels[0].set_value(v0)
		self.reels[1].set_value(v1)
		self.reels[2].set_value(v2)
		self.reels[3].set_value(v3)
		self.reels[4].set_value(v4)
		
	def touch_began(self, touch):
		if not self.started:
			if not self.stopped:
				# Start
				sound.play_effect('ui:switch19')
				self.start_time = time()
				self.started = True
			else:
				# Reset
				sound.play_effect('ui:switch20')
				for reel in self.reels:
					reel.animate_to(0, 0.3)
				self.stopped = False
		else:
			# Stop
			sound.play_effect('ui:switch2')
			self.stopped = True
			self.started = False
			for reel in self.reels:
				reel.animate_to(int(reel.value))
			
if __name__ == '__main__':
	run(StopWatch())