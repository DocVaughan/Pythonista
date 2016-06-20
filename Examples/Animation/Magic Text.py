# coding: utf-8

'''
Draw lines on the screen to reveal the 'Zen of Python' -- or replace it with your own text (by changing the MESSAGE string).
'''

from scene import *
import random
import math
import ui
from colorsys import hsv_to_rgb
A = Action

FONT_NAME = 'Ubuntu Mono'
if min(ui.get_screen_size()) > 750:
	FONT_SIZE = 60
else:
	FONT_SIZE = 30
SPACING = FONT_SIZE * 0.45

MESSAGE = '''The Zen of Python, by Tim Peters
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''

class MyScene (Scene):
	def setup(self):
		self.hue = 0.0
		self.prev_touch = None
		self.letter_index = 0
		self.background_color = '#262b30'
		self.instructions = LabelNode('Draw with one finger.', ('HelveticaNeue-Light', 24), position=self.size/2, parent=self)
	
	def did_change_size(self):
		if self.instructions:
			self.instructions.position = self.size/2

	def touch_began(self, touch):
		if self.instructions:
			self.instructions.run_action(Action.fade_to(0, 1))
			self.instructions = None
		self.prev_touch = touch.location
	
	def touch_moved(self, touch):
		d = touch.location - self.prev_touch
		if abs(d) < SPACING:
			return
		letter_pos = self.prev_touch + 0.5 * d
		self.prev_touch = touch.location
		letter = MESSAGE[self.letter_index]
		self.letter_index += 1
		self.letter_index %= len(MESSAGE)
		if not letter.strip():
			return
		a = -math.atan2(*d) + math.pi/2
		font = (FONT_NAME, FONT_SIZE)
		color = hsv_to_rgb(self.hue, 0.65, 1)
		label = LabelNode(letter, font=font, position=touch.location, color=color)
		label.rotation = a
		self.hue += 0.03
		label.run_action(A.sequence(
			A.move_to(letter_pos.x, letter_pos.y, 1.2, TIMING_ELASTIC_OUT),
			A.wait(3),
			A.scale_to(0, 0.25),
			A.remove()))
		self.add_child(label)
		for i in range(5):
			p = SpriteNode('shp:Spark', position=letter_pos, color=color)
			p.blend_mode = BLEND_ADD
			r = max(FONT_SIZE, 50)
			dx, dy = random.uniform(-r, r), random.uniform(-r, r)
			p.run_action(A.sequence(
				A.group(
					A.scale_to(0),
					A.move_by(dx, dy, 0.5, TIMING_EASE_OUT_2)),
				A.remove()))
			self.add_child(p)

if __name__ == '__main__':
	run(MyScene(), multi_touch=False)
	