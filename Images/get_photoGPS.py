import photos
import webbrowser

query = 'safari-http://maps.apple.com/?q=%s,%s'

img = photos.pick_image(include_metadata=True)

meta = img[1]
gps = meta.get('{GPS}')

if gps:
  latitude = str(gps.get('Latitude', 0.0)) + gps.get('LatitudeRef', '')
  longitude =str(gps.get('Longitude', 0.0)) + gps.get('LongitudeRef', '')
  print '%s, %s' % (latitude, longitude)
  #webbrowser.open(query % (latitude, longitude))
else:
  print 'Last photo has no location metadata.'

