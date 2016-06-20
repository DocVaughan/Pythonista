import appex
from PIL import Image
from PIL.ExifTags import TAGS
import clipboard

def get_exif(fn):
	ret = {}
	i = Image.open(fn)
	info = i._getexif()
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		ret[decoded] = value
	return ret

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	images = appex.get_attachments('public.jpeg')
	if images:
		a = get_exif(images[0])
		if a.get('GPSInfo'):
			lat = [float(x)/float(y) for x, y in a['GPSInfo'][2]]
			latref = a['GPSInfo'][1]
			lon = [float(x)/float(y) for x, y in a['GPSInfo'][4]]
			lonref = a['GPSInfo'][3]
			lat = lat[0] + lat[1]/60 + lat[2]/3600
			lon = lon[0] + lon[1]/60 + lon[2]/3600
			if latref == 'S':
				lat = -lat
			if lonref == 'W':
				lon = -lon
			loc_str = '%f, %f' % (lat, lon)
			print('Latitude/Longitude:')
			print(loc_str)
			clipboard.set(loc_str)
			print('(copied to the clipboard -- you can paste this in the search field of Maps to go to the location where the photo was taken)')
		else:
			print('No location data found')
	else:
		print('No input image found')

if __name__ == '__main__':
	main()