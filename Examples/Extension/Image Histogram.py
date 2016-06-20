from PIL import Image
import appex
import ui

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	img = appex.get_image()
	if not img:
		print('No input image')
		return
	if not img.mode.startswith('RGB'):
		img = img.convert('RGB')
	hist = img.histogram()
	max_h = float(max(hist))
	height = 240
	with ui.ImageContext(512, height) as ctx:
		a = 0.5
		rgb = [(1, 0, 0, a), (0, 1, 0, a), (0, 0, 1, a)]
		for i, color in enumerate(rgb):
			ui.set_color(color)
			for j, count in enumerate(hist[i*256:i*256+256]):
				bar_height = count / max_h * height
				ui.fill_rect(2*j, height-bar_height, 2, bar_height)
		ctx.get_image().show()

if __name__ == '__main__':
	main()