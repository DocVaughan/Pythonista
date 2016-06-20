# coding: utf-8

from scene import *
import sound
from math import sin, cos, pi, ceil
from random import uniform as rnd, choice, randint
from game_menu import MenuScene
from game_levels import levels, colors
from colorsys import hsv_to_rgb
import sys
A = Action

def _cmp(a, b):
	return ((a>b)-(a<b))

if sys.version_info[0] >= 3:
	cmp = _cmp

paddle_speed = 30
min_ball_speed = 10
max_ball_speed = 18
# How much faster the ball gets when it hits a brick:
brick_speedup = 0.15
# How much faster the ball gets when a new level is reached:
level_speedup = 2.0
powerup_chance = 0.1
filter_names = ['None', 'Gray', 'B&W', 'LCD', 'Wavy']

# Helper functions for collision testing:
def closest_point(rect, circle):
	return Point(max(rect.min_x, min(rect.max_x, circle.x)), max(rect.min_y, min(rect.max_y, circle.y)))

def hit_test(rect, circle, radius, bbox=None):
	if bbox and not rect.intersects(bbox):
		return False
	return abs(closest_point(rect, circle) - circle) < radius

# Particle effect when the ball hits a brick:
class Explosion (Node):
	def __init__(self, brick, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.position = brick.position
		for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
			p = SpriteNode(brick.texture, scale=0.5, parent=self)
			p.position = brick.size.w/4 * dx, brick.size.h/4 * dy
			p.size = brick.size
			d = 0.4
			r = 30
			p.run_action(A.move_to(rnd(-r, r), rnd(-r, r), d))
			p.run_action(A.scale_to(0, d))
			p.run_action(A.rotate_to(rnd(-pi/2, pi/2), d))
		self.run_action(A.sequence(A.wait(d), A.remove()))

# Simple SpriteNode subclasses for the different game objects:

class Ball (SpriteNode):
	def __init__(self, v=(0, 0), r=11, *args, **kwargs):
		SpriteNode.__init__(self, 'pzl:BallBlue', *args, **kwargs)
		self.size = (r*2, r*2)
		self.v = Vector2(*v)
		self.r = r
		self.ball_speed = 10.0
		self.last_collision = None
		self.is_new = True
		self.powerup_type = 0
	
	def update_effects(self):
		# If the ball has a powerup, draw a red or blue "tail"
		if not self.powerup_type:
			return
		for i in range(3):
			p = SpriteNode('shp:Spark', z_position=-1, parent=self.parent)
			p.blend_mode = BLEND_ADD
			p.color = '#ff0000'
			angle = rnd(0, pi*2)
			d = rnd(0, self.r-4)
			flame_hue = 0.6 if self.powerup_type == 2 else 0.0
			p.color = hsv_to_rgb((d/self.r)*0.15 + flame_hue, 0.9, 1)
			p.scale = 1.2
			x, y = cos(angle)*d, sin(angle)*d
			p.position = self.position + (x, y)
			p.run_action(A.sequence(A.fade_to(0, 0.2), A.remove()))

class Powerup (SpriteNode):
	def __init__(self, powerup_type, v=(0, 0), *args, **kwargs):
		img = 'spc:PillRed' if powerup_type == 1 else 'spc:PillBlue'
		SpriteNode.__init__(self, img, *args, **kwargs)
		self.powerup_type = powerup_type
		self.v = Vector2(*v)

class Brick (SpriteNode):
	def __init__(self, brick_type, *args, **kwargs):
		img = colors.get(brick_type, 'pzl:Red8')
		SpriteNode.__init__(self, img, *args, **kwargs)
		self.brick_type = brick_type

# The actual game logic:

class Game (Scene):
	def setup(self):
		self.filter = 0
		self.score = 0
		self.level = 0
		self.paddle_powerup = 0
		self.paddle_charge = 0
		self.lives_left = 3
		self.level_start_time = 0
		self.bricks = []
		self.balls = []
		self.powerups = []
		self.ball_r = 11 if self.size.w > 760 else 7
		# Lower ball speed on iPhone (everything is smaller):
		self.speed_scale = 1.0 if self.size.w > 760 else 0.65
		self.effect_node = EffectNode(parent=self)
		with open('filters.fsh') as f:
			self.effect_node.shader = Shader(f.read())
		self.effect_node.crop_rect = self.bounds
		self.effect_node.effects_enabled = False
		
		self.game_node = Node(parent=self.effect_node)
		
		self.top_bg = SpriteNode(parent=self, position=(0, self.size.h))
		self.top_bg.color = '#1c1c1c'
		self.top_bg.size = self.size.w, 90
		self.top_bg.anchor_point = (0, 1)
		
		self.hud_hearts = [SpriteNode('plf:HudHeart_full', position = (30 + i * 32, self.size.h - 65), scale=0.5, parent=self) for i in range(3)]
		self.pause_button = SpriteNode('iow:pause_32', position=(32, self.size.h-32), parent=self)
		paddle_y = 120 if self.size.w > 760 else 70
		self.paddle = SpriteNode('pzl:PaddleBlue', position=(self.size.w/2, paddle_y), parent=self.game_node)
		self.paddle.scale = 1.0 if self.size.w > 760 else 0.7
		self.paddle_target = self.size.w/2
		
		self.score_label = LabelNode('0', font=('Avenir Next', 40), position=(self.size.w/2, self.size.h-50), parent=self)
		right_wall = Rect(self.size.w, 0, 100, self.size.h)
		left_wall = Rect(-100, 0, 100, self.size.h)
		top_wall = Rect(0, self.size.h-90, self.size.w, 100)
		self.walls = [SpriteNode(position=rect.center(), size=rect.size) for rect in (left_wall, right_wall, top_wall)]
		self.background_color = '#292e37'
		self.load_highscore()
		self.show_start_menu()
		
	def load_highscore(self):
		try:
			with open('.brickbreaker_highscore', 'r') as f:
				self.highscore = int(f.read())
		except:
			self.highscore = 0
	
	def save_highscore(self):
		with open('.brickbreaker_highscore', 'w') as f:
			f.write(str(self.highscore))
	
	def new_game(self):
		self.level = 0
		for b in self.bricks:
			b.remove_from_parent()
		self.bricks = []
		for b in self.balls:
			b.remove_from_parent()
		self.balls = []
		self.spawn_ball()
		self.load_level(levels[self.level])
		self.score = 0
		self.lives_left = 3
		self.paddle_powerup = 0
		self.paddle_charge = 0
		for h in self.hud_hearts:
			h.alpha = 1
		self.score_label.text = '0'
	
	def load_level(self, level_str):
		lines = level_str.splitlines()
		if self.size.w > 760:
			#iPad
			brick_w, brick_h = 64, 32
		else:
			#iPhone
			brick_w, brick_h = 32, 16
		min_x = self.size.w/2 - 4.5 * brick_w
		min_y = self.size.h/2 - len(lines) * brick_h/2
		for y, line in enumerate(reversed(lines)):
			for x, char in enumerate(line):
				if char == ' ': continue
				pos = Point(x * brick_w + min_x, min_y + y * brick_h)
				brick = Brick(char, position=pos, parent=self.game_node)
				brick.size = (brick_w, brick_h)
				self.bricks.append(brick)
		for i, b in enumerate(self.bricks):
			b.scale = 0
			b.run_action(A.sequence(A.wait(i*0.01), A.scale_to(1, 0.25, 4)))
		self.level_start_time = self.t
	
	def update(self):
		self.move_paddle()
		self.update_all_balls()
		self.update_powerups()
		if not self.balls:
			self.ball_lost()
		if not self.bricks:
			self.level_finished()
		
	def update_powerups(self):
		for p in list(self.powerups):
			p.position += p.v
			if p.position.y < -50:
				p.remove_from_parent()
				self.powerups.remove(p)
			if self.paddle.frame.intersects(p.frame):
				sound.play_effect('arcade:Powerup_1', 0.25, 0.8)
				p.remove_from_parent()
				self.powerups.remove(p)
				self.paddle_powerup = p.powerup_type
				self.paddle_charge = 3
				if p.powerup_type == 1:
					self.paddle.color = '#ffa7a8'
				else:
					self.paddle.color = '#a7e2ff'

	def update_all_balls(self):
		for ball in list(self.balls):
			ball.update_effects()
			# Update in multiple steps, so a ball cannot pass through a brick in a single frame:
			steps = int(ceil(abs(ball.v)/5.0))
			for i in range(steps):
				self.update_ball(ball, ball.v / steps)
			if ball.position.y < -50:
				self.balls.remove(ball)
				ball.remove_from_parent()
	
	def update_ball(self, ball, v):
		bp = ball.position + v
		ball_r = ball.r
		colliders = self.bricks + self.walls + [self.paddle]
		ball_bbox = Rect(bp.x-ball_r, bp.y-ball_r, ball_r*2, ball_r*2)
		collisions = []
		new_ball = ball.is_new
		for node in colliders:
			if new_ball and node != self.paddle:
				continue
			if node == ball.last_collision:
				continue
			frame = node.frame
			if node == self.paddle:
				# Make the paddle a little larger than it actually is:
				frame = frame.inset(-10, -5, 0, -5)
			if hit_test(frame, bp, ball_r, ball_bbox):
				collisions.append((frame, node))
		if not collisions:
			ball.position = bp
			return
		# Move the ball back where it came from until it doesn't collide anymore:
		while any(hit_test(c[0], bp, ball_r) for c in collisions):
			bp -= (v / abs(v))
		# Find the closest collision point:
		collisions = [(c[1], closest_point(c[0], bp)) for c in collisions]
		sorted_collisions = sorted(collisions, key=lambda x: abs(x[1] - bp))
		collider, p = sorted_collisions[0]
		if isinstance(collider, Brick):
			self.destroy_brick(ball, collider)
			if ball.powerup_type == 2:
				sound.play_effect('digital:Laser5', 0.5)
				return
		self.play_collision_sound(collider)
		ball.last_collision = collider
		side_hit = abs(v.x) > 0 and cmp(bp.x - collider.position.x, 0) != cmp(v.x, 0) and abs(bp.x - p.x) > abs(bp.y - p.y)
		v *= (-1, 1) if side_hit else (1, -1)
		if collider == self.paddle and v.y > 0:
			# Adjust the ball's direction relative to where it hit the paddle
			dx = bp.x - self.paddle.position.x
			paddle_w = self.paddle.size.w
			angle = dx / (paddle_w/3.0) * pi/6
			if abs(angle) < 0.22:
				angle = 0.22 * (cmp(angle, 0) or 1.0)
			v = Vector2(sin(angle), cos(angle))
			ball.powerup_type = self.paddle_powerup
			self.paddle_charge = max(0, self.paddle_charge - 1)
			if self.paddle_charge <= 0:
				self.paddle_powerup = 0
				self.paddle.color = 'white'
		ball.position = bp
		ball.is_new = False
		ball.v = (v/abs(v)) * ball.ball_speed * self.speed_scale
	
	def ball_lost(self):
		sound.play_effect('digital:ZapThreeToneDown')
		self.lives_left -= 1
		for i, heart in enumerate(self.hud_hearts):
			heart.alpha = 1 if self.lives_left > i else 0
		if self.lives_left <= 0:
			self.game_over()
		else:
			self.spawn_ball()
	
	def game_over(self):
		if self.score > self.highscore:
			self.highscore = self.score
			self.save_highscore()
		self.paused = True
		self.menu = MenuScene('Game Over', 'Highscore: %i' % self.highscore, ['New Game', 'Filter: ' + filter_names[self.filter]])
		self.present_modal_scene(self.menu)
		
	def level_finished(self):
		self.score += max(0, 100-int(self.t - self.level_start_time)) * (self.level+1)
		self.score_label.text = str(self.score)
		self.level += 1
		sound.play_effect('digital:ZapThreeToneUp')
		for b in self.balls:
			b.remove_from_parent()
		self.balls = []
		for p in self.powerups:
			p.remove_from_parent()
		self.powerups = []
		self.spawn_ball()
		self.load_level(levels[self.level % len(levels)])
	
	def spawn_ball(self):
		new_ball = Ball(r=self.ball_r, v=(0, -1), position=(self.size.w/2, self.paddle.position.y + 100), parent=self.game_node)
		new_ball.scale = 0
		new_ball.run_action(A.scale_to(1, 0.3))
		new_ball.ball_speed = min(max_ball_speed, min_ball_speed + level_speedup * self.level)
		self.balls.append(new_ball)
	
	def destroy_brick(self, ball, brick, with_powerup=True):
		brick.remove_from_parent()
		self.bricks.remove(brick)
		self.game_node.add_child(Explosion(brick))
		self.score += 10 * (self.level + 1)
		self.score_label.text = str(self.score)
		ball.ball_speed = min(max_ball_speed, ball.ball_speed + brick_speedup)
		if with_powerup and ball.powerup_type == 1:
			sound.play_effect('digital:Laser3')
			for b in list(self.bricks):
				if abs(b.position - ball.position) < brick.size.w * 1.5:
					self.destroy_brick(ball, b, False)
		spawn_powerup = rnd(0.0, 1.0) <= powerup_chance and ball.powerup_type == 0
		if spawn_powerup:
			self.spawn_powerup(ball, brick)
	
	def spawn_powerup(self, ball, brick):
		sound.play_effect('digital:PhaserUp5')
		powerup_type = randint(1, 4)
		if powerup_type == 3:
			# Two small extra balls
			for dx in (-8, 8):
				new_ball = Ball(r=self.ball_r/2, position=brick.position + (dx, 0), parent=self.game_node)
				new_ball.ball_speed = ball.ball_speed
				self.balls.append(new_ball)
				new_ball.v = Vector2(0, -new_ball.ball_speed/2)
		elif powerup_type == 4:
			# One regular extra ball
			new_ball = Ball(r=self.ball_r, position=brick.position, parent=self.game_node)
			new_ball.ball_speed = ball.ball_speed
			self.balls.append(new_ball)
			new_ball.v = Vector2(0, -new_ball.ball_speed/2)
		else:
			# Blue/red pill
			p = Powerup(powerup_type, v=(0, -ball.ball_speed/2))
			p.position = brick.position
			p.scale = 1.0 if self.size.w > 760 else 0.7
			p.z_position = 2
			self.powerups.append(p)
			self.game_node.add_child(p)
	
	def play_collision_sound(self, collider):
		if isinstance(collider, Brick):
			sound.play_effect('8ve:8ve-beep-roadblock')
		elif collider == self.paddle:
			if self.paddle_powerup:
				sound.play_effect('digital:Laser2')
			else:
				sound.play_effect('8ve:8ve-beep-shinymetal')
		else:
			sound.play_effect('8ve:8ve-tap-mellow')
		
	def move_paddle(self):
		dx = self.paddle_target - self.paddle.position.x
		if abs(dx) > paddle_speed:
			dx = paddle_speed * cmp(dx, 0)
		self.paddle.position += dx, 0
	
	def touch_began(self, touch):
		x, y = touch.location
		if x < 48 and y > self.size.h - 48:
			self.show_pause_menu()
		else:
			self.paddle_target = x / self.game_node.scale
	
	def touch_moved(self, touch):
		self.paddle_target = touch.location.x / self.game_node.scale
	
	def show_start_menu(self):
		self.paused = True
		self.menu = MenuScene('BrickBreaker', 'Highscore: %i' % self.highscore, ['Play', 'Filter: ' + filter_names[self.filter]])
		self.present_modal_scene(self.menu)
	
	def show_pause_menu(self):
		self.paused = True
		self.menu = MenuScene('Paused', 'Highscore: %i' % self.highscore, ['Continue', 'New Game', 'Filter: ' + filter_names[self.filter]])
		self.present_modal_scene(self.menu)
	
	def menu_button_selected(self, title):
		if title.startswith('Filter:'):
			self.filter = (self.filter + 1) % len(filter_names)
			if self.filter == 0:
				# No filter
				self.effect_node.effects_enabled = False
				self.background_color = '#292e37'
			else:
				# The shader (defined in filters.fsh) decides which filter to use based on this uniform:
				self.effect_node.shader.set_uniform('u_style', self.filter)
				self.effect_node.effects_enabled = True
				if self.filter in (1, 2):
					self.background_color = '#333'
				elif self.filter == 3:
					self.background_color = '#474e3b'
				else:
					self.background_color = '#292e37'
			return 'Filter: ' + filter_names[self.filter]
		elif title in ('Continue', 'New Game', 'Play'):
			self.dismiss_modal_scene()
			self.menu = None
			self.paused = False
			if title in ('New Game', 'Play'):
				self.new_game()

# Run the game:
if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=False)
