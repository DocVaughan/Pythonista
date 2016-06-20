# coding: utf-8

'''
Demo of creating an animated GIF from a sequence of images

* Based on the blog post "Vector Animations with Python" by @Zulko (http://zulko.github.io/blog/2014/09/20/vector-animations-with-python/)
* Adapted for Pythonista/iOS by Luke Taylor (forum post: https://forum.omz-software.com/topic/2052/gif-art-in-python)
'''

from PIL import Image, ImageDraw
from images2gif import writeGif
from math import sin, cos, pi
import console

# You can adjust these values to produce a larger and/or smoother animation (that requires more memory):
size = 100
duration = 2.0
n_frames = 30
n_circles = 20

def make_frame(t):
	# Render at a larger size and scale down afterwards (for smoother edges):
	r_size = size * 3
	img = Image.new('RGB', (r_size, r_size), 'white')
	surface = ImageDraw.Draw(img)
	for i in range(n_circles):
		angle = 2 * pi * (float(i) / n_circles + t)
		center_x = r_size * (0.5 + cos(angle) * 0.1)
		center_y = r_size * (0.5 + sin(angle) * 0.1)
		r = r_size * (1.0 - float(i) / n_circles)
		bbox = (center_x - r, center_y - r, center_x + r, center_y + r)
		color = 3 * (i % 2 * 255,)
		surface.ellipse(bbox, fill=color)
	return img.resize((size, size), Image.ANTIALIAS)
	
def main():
	images = [make_frame(float(i)/n_frames) for i in range(n_frames)]
	writeGif('animation.gif', images, duration/n_frames)
	console.quicklook('animation.gif')
	
if __name__ == '__main__':
	main()