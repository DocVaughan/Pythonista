from scene import *
from random import random
import socket

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		
		# set up UDP socket - IP address and socket to send to
		#self.HOST, self.PORT = '130.70.157.125', 2390
		#self.HOST, self.PORT = '10.0.1.114', 2390
		#self.HOST, self.PORT = '192.168.0.101', 2390

		self.HOST, self.PORT = '192.168.1.133', 2390

		# SOCK_DGRAM is the socket type to use for UDP sockets
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


		# Set up the root layer and one other layer:
		self.root_layer = Layer(self.bounds)
		center = self.bounds.center()
		

		#right track area
		self.layerRight = Layer(Rect(self.size.w*(1-1/8.), center.y-self.size.h/4, self.size.w/8, self.size.h/2))
		self.layerRight.background = Color(1., 0, 0)
		self.root_layer.add_layer(self.layerRight)
		
		self.markRight = Layer(Rect(self.size.w*(1-1/8.), center.y-self.size.h/32, self.size.w/8, self.size.h/16))
		self.markRight.background = Color(0.2, 0.2, 0.2)
		self.root_layer.add_layer(self.markRight)
	
		#left track area
		self.layerLeft = Layer(Rect(0, center.y-self.size.h/4, self.size.w/8, self.size.h/2))
		self.layerLeft.background = Color(1., 0., 0.)
		self.root_layer.add_layer(self.layerLeft)
		
		self.markLeft = Layer(Rect(0, center.y-self.size.h/32, self.size.w/8, self.size.h/16))
		self.markLeft.background = Color(0.2, 0.2, 0.2)
		self.root_layer.add_layer(self.markLeft)
		
		self.right_touchID = []
		self.left_touchID = []
		
		self.valueLeft = 0
		self.valueRight = 0
		self.data = (self.valueLeft, self.valueRight)
		
	
	
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0.75, 0.75, 0.75)
		
		data_str = str(int(self.data[0]*100))+ ', ' + str(int(self.data[1]*100))

		# send the slider values as a comma separated pair
		self.sock.sendto(data_str.encode('utf-8'), (self.HOST, self.PORT))
		
		# show current output
		text('Output = {:3.0f}, \t{:3.0f}'.format(self.data[0]*100, self.data[1]*100), font_name='Helvetica', font_size=28.0, x=self.size.w/2., y=50., alignment=5)

		# Show the output on the screen
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		
	
	def touch_began(self, touch):
		# Animate the layer to the location of the touch:

		if touch.location in self.layerLeft.frame:
			self.initialLeft = touch.location
			self.left_touchID = touch

			# Animate the background color to a random color:
			#new_color = Color(random(), random(), random())
			#self.layerLeft.animate('background', new_color, 1.0)
			self.currentLeft = touch.location
			valueLeft = (self.currentLeft.y - self.size.h/2) / (self.layerLeft.frame.h/2.)
			#new_color = Color(math.fabs(self.valueLeft), 1-math.fabs(self.valueLeft), 0.)

			new_frame = Rect(0, self.currentLeft.y-self.size.h/32, self.size.w/8, self.size.h/16)
			self.markLeft.animate('frame', new_frame, 0.5)

		else: 
			self.valueLeft = 0.
			#new_color = Color(1-math.fabs(self.valueLeft), 0., 0.)
		#print(valueLeft)

		#self.layerLeft.animate('background', new_color, 0.01)
	
		if touch.location in self.layerRight.frame:
			self.initialRight = touch.location
			self.right_touchID = touch
			
			#new_frame = Rect(x - 64, y - 64, 128, 128)
			#self.layerLeft.animate('frame', new_frame, 1.0, curve=curve_bounce_out)
			# Animate the background color to a random color:
			#new_color = Color(random(), random(), random())
			#self.layerRight.animate('background', new_color, 1.0)
			self.currentRight = touch.location
			self.valueRight = (self.currentRight.y - self.size.h/2) / (self.layerRight.frame.h/2.)
			#new_color = Color(abs(valueLeft), 0., 0.)

			new_frame = Rect(self.size.w*(1-1/8.), self.currentRight.y-self.size.h/32, self.size.w/8, self.size.h/16)
			self.markRight.animate('frame', new_frame, 0.5)

		else: 
			self.valueRight = 0.
		
		self.data = (self.valueLeft, self.valueRight)
			
			
	
	def touch_moved(self, touch):
		
		#hack for now
		center = self.bounds.center()
		
		#if touch.location in self.layerLeft.frame:
		if touch == self.left_touchID:
			self.currentLeft = touch.location
			
			# limit to bounds of slider and value
			if self.currentLeft.y > center.y + self.size.h/4:
				self.currentLeft.y = center.y + self.size.h/4
			elif self.currentLeft.y < center.y - self.size.h/4:
				self.currentLeft.y = center.y - self.size.h/4
			
			self.valueLeft = (self.currentLeft.y - self.size.h/2) / (self.layerLeft.frame.h/2.)
			
			#new_color = Color(math.fabs(self.valueLeft), 1-math.fabs(self.valueLeft), 0.)
			
			new_frame = Rect(0, self.currentLeft.y-self.size.h/32, self.size.w/8, self.size.h/16)
			self.markLeft.animate('frame', new_frame, 1.0/60)
			
			#self.layerLeft.animate('background', new_color, 0.01)
		
		
		#if touch.location in self.layerRight.frame:
		if touch == self.right_touchID:
			self.currentRight = touch.location
			
			# limit to bounds of slider and value
			if self.currentRight.y > center.y + self.size.h/4:
				self.currentRight.y = center.y + self.size.h/4
			elif self.currentRight.y < center.y - self.size.h/4:
				self.currentRight.y = center.y - self.size.h/4
			
			self.valueRight = (self.currentRight.y - self.size.h/2) / (self.layerRight.frame.h/2.)
			
			new_frame = Rect(self.size.w*(1-1/8.), self.currentRight.y-self.size.h/32, self.size.w/8, self.size.h/16)
			self.markRight.animate('frame', new_frame, 1.0/60)
		
		self.data = (self.valueLeft, self.valueRight)
		
	
	def touch_ended(self, touch):
		
		if touch == self.right_touchID:
			# move right back to center
			new_frame = Rect(self.size.w*(1-1/8.), self.size.h/2 - self.size.h/32, self.size.w/8, self.size.h/16)
			self.markRight.animate('frame', new_frame, 0.25)		
			self.valueRight = 0
			self.right_touchID = []

		if touch == self.left_touchID:
			# move left back to center
			new_frame = Rect(0, self.size.h/2 - self.size.h/32, self.size.w/8, self.size.h/16)
			self.markLeft.animate('frame', new_frame, 0.25)
			self.valueLeft = 0
			self.left_touchID = []
			
			new_color = Color(1.0, 0.0, 0.0)
			self.layerLeft.animate('background', new_color, 0.01)             
		
		self.data = (self.valueLeft, self.valueRight)
		
if __name__ == '__main__':
	run(MyScene())
