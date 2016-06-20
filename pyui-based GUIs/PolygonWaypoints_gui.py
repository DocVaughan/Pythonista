# coding: utf-8
import json
import time, datetime
import sys
import location, motion
import socket

import ui

import numpy as np

import geographic_calculations as geoCalc

class MyView (ui.View):
	def __init__(self):
		# This will also be called without arguments when the view is loaded from a UI file.
		# You don't have to call super. Note that this is called *before* the attributes
		# defined in the UI file are set. Implement `did_load` to customize a view after
		# it's been fully loaded from a UI file.
		#self.waypoints = []#np.zeros((1,2))
		pass


	def did_load(self):
		# This will be called when a view has been fully loaded from a UI file.
		self.present('sheet')
		
		# set up UDP socket - IP address and socket to send to
		self.HOST, self.PORT = '192.168.0.101', 2390

		# SOCK_DGRAM is the socket type to use for UDP sockets
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def will_close(self):
		# This will be called when a presented view is about to be dismissed.
		# You might want to save data here.
		location.stop_updates()
		motion.stop_updates()

	def draw(self):
		# This will be called whenever the view's content needs to be drawn.
		# You can use any of the ui module's drawing functions here to render
		# content into the view's visible rectangle.
		# Do not call this method directly, instead, if you need your view
		# to redraw its content, call set_needs_display().
		# Example:
		pass

	def layout(self):
		# This will be called when a view is resized. You should typically set the
		# frames of the view's subviews here, if your layout requirements cannot
		# be fulfilled with the standard auto-resizing (flex) attribute.
		pass

	def touch_began(self, touch):
		# Called when a touch begins.
		pass

	def touch_moved(self, touch):
		# Called when a touch moves.
		pass

	def touch_ended(self, touch):
		# Called when a touch ends.
		pass

	def keyboard_frame_will_change(self, frame):
		# Called when the on-screen keyboard appears/disappears
		# Note: The frame is in screen coordinates.
		pass

	def keyboard_frame_did_change(self, frame):
		# Called when the on-screen keyboard appears/disappears
		# Note: The frame is in screen coordinates.
		pass
	
	
# As a function:
#def button_tapped(sender):
#    print 'button tapped'
#
# As a method:
#class MyButtonHandler (object):
#    def button_tapped(self, sender):
#        print 'button tapped'

def add_waypoint(sender):
	if v['switch1'].value:
		current = location.get_location()

		curr_location = np.array([current['latitude'], current['longitude']])
		
		heading = calculate_heading(mag)
	
		num_sides = int(v['num_sides'].text)
		dist_per_side = int(v['dist_per_side'].text)
		
		v.waypoints = geoCalc.get_polygon_waypoints(curr_location, heading, num_sides, dist_per_side)
		
		v['waypointList'].text = repr(v.waypoints)
	else:
		pass
		
def send_waypoints(sender):
	if v['waypointList'].text:
		json_waypoints = json.dumps(v.waypoints.tolist())
		
		# send the velocity as x, y pair
		v.sock.sendto(json_waypoints.encode('utf-8'), (v.HOST, v.PORT))
	
	else:
		pass
	

def calculate_heading(mag_data):
      ''' function calculates heading assuming'''
      heading = (360.0 - np.arctan2(mag_data[1], mag_data[0]) * 180.0/np.pi) % 360 
      
      return heading

if __name__ ==  '__main__':
	v = ui.load_view('PolygonWaypoints_gui')


	last_time=time.time()
	while v.on_screen:
		try: 
			if v['switch1'].value:
				v['datetime'].text = str(datetime.datetime.now())
				
				location.start_updates()
				motion.start_updates()
			
				delta_t = time.time() - last_time

				if delta_t > 1.:
		
					current = location.get_location()
					mag = motion.get_magnetic_field()
				
					heading = calculate_heading(mag)
		
					#print current
					latitude = current['latitude']
					longitude = current['longitude']
					if current['speed'] != 0:
						bearing = current['course']
					else:
						bearing = np.nan
				
					v['heading'].text = '{:.0f}'.format(heading)
					v['bearing'].text = '{:.0f}'.format(bearing)
					v['latitude'].text = '{:10.6f}'.format(float(latitude))
					v['longitude'].text = '{:10.6f}'.format(float(longitude))
		
					last_time = time.time()
					current = None 

			else:
				location.stop_updates()
				motion.stop_updates()
		
			time.sleep(0.1)
			
		except (KeyboardInterrupt, SystemExit): 
			location.stop_updates()
			motion.stop_updates()
			break 
			time.sleep(1)

