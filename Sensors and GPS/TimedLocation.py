import console
import time
import location

location.start_updates()
time.sleep(3)

last_time=time.time()

while True:
#	current = location.get_location()
#		
#	long_lat = str(current['timestamp']) + ', ' + str(current['latitude']) + ', ' + str(current['longitude'])
#	
#	print long_lat
		
	delta_t = time.time() - last_time

	if delta_t > 3.:
		
		current = location.get_location()
		
		long_lat = str(current['timestamp']) + ', ' + str(current['latitude']) + ', ' + str(current['longitude'])
		
		print long_lat
		
		#location.stop_updates()
		
		last_time = time.time()
		current = None 
		
		location.stop_updates()
		location.start_updates()
