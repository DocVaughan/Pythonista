# coding: utf-8

'''
This example uses the MPMediaQuery API to gather data about your music library, and then prints a list of artists with corresponding song counts.
'''

from objc_util import *
from collections import Counter

NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
MPMediaQuery = ObjCClass('MPMediaQuery')
query = MPMediaQuery.songsQuery()

print('Gathering data...')
artist_counter = Counter()
for item in query.items():
	artist = str(item.valueForKey_('artist'))
	artist_counter[artist] += 1
if len(artist_counter) == 0:
	print('You don\'t seem to have any music in your library.')
else:
	print('Most common artists in your music library:')
	print('=' * 40)
	for i, (artist, count) in enumerate(artist_counter.most_common(10)):
		print('%i. %s (%i songs)' % (i+1, artist, count))