# coding: utf-8
from scene import *
from random import choice, uniform, shuffle
import sound
from itertools import product
from math import sqrt, pi
from game_menu import MenuScene
A = Action

screen_size = min(get_screen_size())
if screen_size > 600:
	COLS, ROWS = 12, 12
	SCALE = 1.0
else:
	COLS, ROWS = 10, 10
	SCALE = (screen_size - 10) / (COLS * 48.0)
game_duration = 60
colors = ['pzl:Blue5', 'pzl:Green5', 'pzl:Purple5', 'pzl:Red6', 'pzl:Yellow6']

class Emitter (Node):
	def __init__(self, img):
		for i in range(3):
			p = SpriteNode(img, position=(uniform(-10, 10), uniform(-10, 10)), scale=uniform(0.5, 1))
			p.run_action(A.move_by(uniform(-75, 75), uniform(-75, 75), 1, 4))
			p.run_action(A.scale_to(0.0, 0.75))
			p.run_action(A.rotate_by(uniform(-pi*2, pi*2), 1))
			p.blend_mode = BLEND_ADD
			self.add_child(p)
		self.run_action(A.sequence(A.wait(1), A.remove()))

class Tile (SpriteNode):
	def __init__(self, img, col=0, row=0):
		SpriteNode.__init__(self, img, position=((col-0.5*COLS)*48 + 24, (row-0.5*ROWS)*48 + 24))
		self.img_name = img
		self.selected = False
		self.grid_pos = (col, row)
	
	def __setattr__(self, name, value):
		SpriteNode.__setattr__(self, name, value)
		if name == 'selected':
			self.run_action(A.scale_to(0.75 if value else 1, 0.15))
		
class Game (Scene):
	def setup(self):
		self.root_node = Node(parent=self)
		self.score = 0
		self.highscore = self.load_highscore()
		self.last_move_t = 0
		score_font = ('Avenir Next', 40)
		time_font = ('Avenir Next Condensed', 32)
		self.score_label = LabelNode('0', font=score_font, parent=self)
		self.score_label.anchor_point = (0.5, 1)
		self.time_label = LabelNode('00:00', font=time_font, parent=self)
		self.time_label.anchor_point = (0, 1)
		self.background_color = '#062a41'
		self.start_time = self.t
		self.pause_button = SpriteNode('iow:pause_32', position=(32, self.size.h-36), parent=self)
		self.run_action(A.sequence(A.wait(0.5), A.call(self.show_start_menu)))
		self.did_change_size()
	
	def load_highscore(self):
		try:
			with open('.Match3Highscore', 'r') as f:
				return int(f.read())
		except:
			return 0
	
	def did_change_size(self):
		self.root_node.position = self.size/2
		self.score_label.position = (self.size.w/2, self.size.h - 10)
		self.time_label.position = (60, self.size.h - 10)
		self.pause_button.position = (32, self.size.h-32)
		
	def update(self):
		if self.t - self.last_move_t > 5:
			self.show_hint()
		sec_left = max(0, game_duration - int(self.t - self.start_time))
		self.time_label.text = '%02d:%02d' % (sec_left/60, sec_left%60)
		if sec_left == 0:
			self.end_game()
	
	def end_game(self):
		if self.score > self.highscore:
			with open('.Match3Highscore', 'w') as f:
				f.write(str(self.score))
			self.highscore = self.score
		sound.play_effect('digital:ZapTwoTone')
		self.show_game_over_menu()
	
	def new_game(self):
		self.root_node.run_action(A.sequence(A.fade_to(0, 0.35), A.remove()))
		self.score = 0
		self.score_label.text = '0'
		self.start_time = self.t
		self.root_node = Node(parent=self, position=self.size/2)
		self.root_node.scale = 0
		self.tiles = []
		for y, x in product(range(ROWS), range(COLS)):
			img_name = choice(colors)
			s = Tile(img_name, x, y)
			self.root_node.add_child(s)
			self.tiles.append(s)
		self.root_node.run_action(A.scale_to(SCALE, 0.35, TIMING_EASE_OUT_2))
		sound.play_effect('digital:ZapThreeToneUp')
	
	def reset_board(self):
		for i, t in enumerate(self.tiles):
			t.run_action(A.sequence(A.fade_to(0, 0.3), A.remove()))
			new_tile = Tile(choice(colors))
			new_tile.grid_pos = t.grid_pos
			new_tile.position = t.position
			new_tile.scale = 0
			new_tile.run_action(A.scale_to(1, 0.5, TIMING_EASE_OUT_2))
			self.root_node.add_child(new_tile)
			self.tiles[i] = new_tile
	
	def show_hint(self):
		self.last_move_t = self.t
		shuffled_tiles = list(self.tiles)
		shuffle(shuffled_tiles)
		for t in shuffled_tiles:
			visited = set()
			count = self.count_from(t, visited)
			if len(visited) >= 3:
				for s in visited:
					s.run_action(A.repeat(
						A.sequence(A.fade_to(0.1, 0.25), A.fade_to(1, 0.25)), 3))
				break
		else:
			self.reset_board()
	
	def touch_began(self, touch):
		if touch.location.x < 48 and touch.location.y > self.size.h - 48:
			self.show_pause_menu()
			return
		selected = [s for s in self.tiles if s.selected]
		if selected:
			return
		t = self.tile_for_touch(touch)
		if t:
			sound.play_effect('ui:click2')
			self.select_from(t)
	
	def touch_ended(self, touch):
		selected = [s for s in self.tiles if s.selected]
		if not selected:
			return
		if len(selected) < 3:
			for t in selected:
				t.selected = False
			sound.play_effect('ui:switch35')
		else:
			sound.play_effect('arcade:Coin_5', 0.15)
			added_score = int((len(selected) * (len(selected) + 1) / 2) * 10)
			self.score += added_score
			self.score_label.text = str(self.score)
			self.show_points(added_score, selected[-1].position)
			self.remove_selected_tiles()
			self.last_move_t = self.t
	
	def show_pause_menu(self):
		self.paused = True
		self.menu = MenuScene('Paused', 'Highscore: %i' % self.highscore, ['Continue', 'New Game'])
		self.present_modal_scene(self.menu)
	
	def show_start_menu(self):
		self.paused = True
		self.menu = MenuScene('Match3', 'Highscore: %i' % self.highscore, ['New Game'])
		self.present_modal_scene(self.menu)
		
	def show_game_over_menu(self):
		self.paused = True
		self.menu = MenuScene('Time Up!', 'Score: %i' % (self.score), ['New Game'])
		self.present_modal_scene(self.menu)
	
	def menu_button_selected(self, title):
		if title.startswith('Retro Mode'):
			self.retro_mode = not self.retro_mode
			self.root_node.shader = self.retro_shader if self.retro_mode else None
			return 'Retro Mode: ' + ('On' if self.retro_mode else 'Off')
		elif title in ('Continue', 'New Game'):
			self.dismiss_modal_scene()
			self.menu = None
			self.paused = False
			if title == 'New Game':
				self.new_game()
	
	def show_points(self, points, pos):
		label = LabelNode('+%i' % (points,), font=('Avenir Next Condensed', 40), position=pos, z_position=1)
		label.run_action(A.sequence(A.wait(0.5), A.fade_to(0, 0.5)))
		label.run_action(A.sequence(A.move_by(0, 100, 1), A.remove()))
		self.root_node.add_child(label)
	
	def tile_for_touch(self, touch):
		touch_pos = self.root_node.point_from_scene(touch.location)
		for t in self.tiles:
			if t.frame.contains_point(touch_pos):
				return t
	
	def tile_at(self, x, y):
		if 0 <= x < COLS and 0 <= y < ROWS:
			return self.tiles[y*COLS+x]
		return None
	
	def remove_selected_tiles(self):
		new_tiles = []
		for col in range(COLS):
			drop = 0
			for row in range(ROWS):
				t = self.tile_at(col, row)
				if t.selected:
					drop += 1
				else:
					t.grid_pos = (t.grid_pos[0], max(0, t.grid_pos[1] - drop))
			for i in range(drop):
				row = ROWS - i - 1
				new_tile = Tile(choice(colors), col, row)
				new_tile.position = (24 + (col - 0.5*COLS) * 48,
					24 + (row - 0.5*ROWS) * 48 + drop * 48)
				new_tile.alpha = 0
				new_tile.run_action(A.fade_to(1.0, 0.35))
				new_tiles.append(new_tile)
				self.root_node.add_child(new_tile)
		all_tiles = self.tiles + new_tiles
		self.tiles = [None] * (ROWS * COLS)
		for t in all_tiles:
			if t.selected:
				t.run_action(A.sequence(A.fade_to(0.0, 0.15), A.remove()))
				e = Emitter(t.img_name)
				e.position = t.position
				self.root_node.add_child(e)
			else:
				x, y = t.grid_pos
				self.tiles[y*COLS+x] = t
				dy = t.position.y - (y * 48 - ROWS * 24 + 24)
				if dy > 0:
					t.run_action(A.move_by(0, -dy, sqrt(dy/750.0), TIMING_EASE_IN_2))
	
	def neighbors(self, tile):
		result = []
		x, y = tile.grid_pos
		directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
		for direction in directions:
			neighbor = self.tile_at(x+direction[0], y+direction[1])
			if neighbor and neighbor.img_name == tile.img_name:
				result.append(neighbor)
		return result
	
	def count_from(self, tile, visited, count=1):
		visited.add(tile)
		neighbors = self.neighbors(tile)
		for n in neighbors:
			if not n in visited:
				visited.add(n)
				count += self.count_from(n, visited, count+1)
		return count
	
	def select_from(self, tile):
		tile.selected = True
		neighbors = self.neighbors(tile)
		for n in neighbors:
			if not n.selected:
				n.selected = True
				self.select_from(n)

if __name__ == '__main__':
	if min(get_screen_size()) < 760:
		# portrait-only on iPhone
		run(Game(), PORTRAIT)
	else:
		# allow any orientation on iPad
		run(Game())
