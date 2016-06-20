'''
A simple analog clock made of ShapeNodes.
'''

from scene import *
from math import pi, sin, cos
from datetime import datetime

class Clock (Scene):
	def setup(self):
		r = min(self.size)/2 * 0.9
		circle = ui.Path.oval(0, 0, r*2, r*2)
		circle.line_width = 6
		shadow = ('black', 0, 0, 15)
		self.face = ShapeNode(circle, 'white', 'silver', shadow=shadow)
		self.add_child(self.face)
		for i in range(12):
			label = LabelNode(str(i+1), font=('HelveticaNeue-UltraLight', 0.2*r))
			label.color = 'black'
			a = 2 * pi * (i+1)/12.0
			label.position = sin(a)*(r*0.85), cos(a)*(r*0.85)
			self.face.add_child(label)
		self.hands = []
		hand_attrs = [(r*0.6, 8, 'black'), (r*0.9, 8, 'black'), (r*0.9, 4, 'red')]
		for l, w, color in hand_attrs:
			shape = ShapeNode(ui.Path.rounded_rect(0, 0, w, l, w/2), color)
			shape.anchor_point = (0.5, 0)
			self.hands.append(shape)
			self.face.add_child(shape)
		self.face.add_child(ShapeNode(ui.Path.oval(0, 0, 15, 15), 'black'))
		self.did_change_size()
		
	def did_change_size(self):
		self.face.position = self.size/2
		
	def update(self):
		t = datetime.now()
		tick = -2 * pi / 60.0
		seconds = t.second + t.microsecond/1000000.0
		minutes = t.minute + seconds/60.0
		hours = (t.hour % 12) + minutes/60.0
		self.hands[0].rotation = 5 * tick * hours
		self.hands[1].rotation = tick * minutes
		self.hands[2].rotation = tick * seconds
		
run(Clock())