'''
Downloads the NASA's "Image of the Day" using the feedparser module.
The image is shown in the console, from where you can save it to
the camera roll, if you like.
'''

import feedparser
from PIL import Image
import sys
if sys.version_info[0] >= 3:
	from urllib.request import urlretrieve
else:
	from urllib import urlretrieve

def main():
	feed = feedparser.parse('http://nasa.gov/rss/dyn/lg_image_of_the_day.rss')
	latest = feed['entries'][0]
	title = latest['title']
	description = latest['summary']
	print('%s\n\n%s' % (title, description))
	links = latest['links']
	image_url = None
	for link in links:
		if link.get('type').startswith('image'):
			image_url = link.get('href')
	if image_url:
		urlretrieve(image_url, 'ImageOfTheDay.jpg')
		img = Image.open('ImageOfTheDay.jpg')
		img.show()
		print('Tap the image to open a full-screen view. Tap and hold to save it to the camera roll.')

if __name__ == '__main__':
	main()