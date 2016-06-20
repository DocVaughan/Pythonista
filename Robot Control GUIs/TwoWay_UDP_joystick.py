from scene import *
import socket, select
import sound
import time, sys, console
import threading
import socketserver
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


data_recieved = ', , , '

#class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
#   """
#   The RequestHandler class for our server.
#
#   It is instantiated once per connection to the server, and must
#   override the handle() method to implement communication to the
#   client.
#   """
#
#   def handle(self):
#       global data_recieved
#       data = self.request[0].strip()
#       socket = self.request[1]
#       #string_to_print = "Velocity from {}: ".format(self.client_address[0]) + data
#
#       data_recieved = data
#       #logging.debug('received data')
#       #logging.debug(string_to_print)
#       #socket.sendto(string_to_print, self.client_address)

# Streaming?... change above to SocketServer.StreamRequestHandler
#     def handle(self):
#         # self.rfile is a file-like object created by the handler;
#         # we can now use e.g. readline() instead of raw recv() calls
#         self.data = self.rfile.readline().strip()
#         print "{} wrote:".format(self.client_address[0])
#         print self.data
#         # Likewise, self.wfile is a file-like object used to write back
#         # to the client
#         self.wfile.write(self.data.upper())


#class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
#   pass



class MyScene(Scene):
    global data_recieved

    def setup(self):
        # This will be called before the first frame is drawn.
        # Set up the root layer and one other layer:
        self.root_layer = Layer(self.bounds)
        center = self.bounds.center()

        # Layer for the joystick "bubble"
        self.layer = Layer(Rect(center.x - 64, center.y - 64, 128, 128))
        self.layer.image = 'White_Circle'
        self.root_layer.add_layer(self.layer)

        # define points for initial touch and current touch location
        self.current = Point()

        # both desired velocities are initially zero
        self.velocity = Point(x=0, y=0)

        # set up UDP socket - IP address and socket to send to
        self.HOST, self.PORT = '172.31.167.207', 2390
        # self.HOST, self.PORT = '10.0.1.114', 2390
        # self.HOST, self.PORT = '192.168.0.101', 2390

        # SOCK_DGRAM is the socket type to use for UDP sockets
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        # set up the receiving thread
        # Port 0 means to select an arbitrary unused port

        # Dr. Vaughan's Apartment
        # HOST, PORT = "10.0.1.102", 2390

        # UWIN
        # HOST, PORT = "172.31.203.109", 2390

        # HOST, PORT = "localhost", 2390

        # Set up receiving via a UDP broadcast
        Broadcast_port = 2390 # where do you expect to get a msg?
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', Broadcast_port))
        self.s.setblocking(0)
#               self.server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
#               ip, port = self.server.server_address
#
#               # Start a thread with the server
#               self.server_thread = threading.Thread(target=self.server.serve_forever)
#               # Exit the server thread when the main thread terminates
#               self.server_thread.daemon = True
#               self.server_thread.start()
        # print "Server loop running in thread:", server_thread.name
        self.receive_broadcast = True
        self.broadcast_thread = threading.Thread(target=self.receive_UDP_broadcast)
        # Exit the server thread when the main thread terminates
        self.broadcast_thread.setDaemon(True)
        self.broadcast_thread.start()




    def draw(self):
        # Update and draw our root layer. For a layer-based scene, this
        # is usually all you have to do in the draw method.
        background(0.75, 0.75, 0.75) # light gray
        self.root_layer.update(self.dt)
        self.root_layer.draw()

        # format a data string to send
        data = self.velocity.as_tuple()
        data_str = str(data[0]) + ', ' + str(data[1])

        # send the velocity as x, y pair
        self.sock.sendto(data_str.encode('utf-8'), (self.HOST, self.PORT))

        # Show the output on the screen
        text('Output = ' + data_str, font_name='Helvetica', font_size=28.0, x=self.size.w/2., y=50., alignment=5)


        lat, lon, heading, speed = data_recieved.rsplit(', ')
        text('Lat: \nLong: \nSpeed: \nHeading:', font_name='SourceCodePro-Regular', font_size=20.0, x=5, y=5., alignment = 9)

        text(' ' + str(lat) + '\n' + str(lon) + '\n  ' + speed + '\n ' + heading, font_name='SourceCodePro-Regular', font_size=20.0, x=105, y=5., alignment = 9)



    def receive_UDP_broadcast(self):
        global data_recieved
        bufferSize = 1024
        while self.receive_broadcast:
            result = select.select([self.s],[],[])
            data_recieved = result[0][0].recv(bufferSize)
            # logging.debug(data_recieved)
            time.sleep(0.1)

    def touch_began(self, touch):
        # Animate the layer to the location of the touch:
        self.current = touch.location

        # if the touch is in the "bubble" then
        if touch.location in self.layer.frame:

            sound.play_effect('Coin_3')
            # Set up a new frame based on latest touch location
            new_frame = Rect(self.current.x - 64, self.current.y - 64, 128, 128)
            self.layer.animate('frame', new_frame)
        else:
            sound.play_effect('Error')
            time.sleep(0.25)
            sound.play_effect('Error')

    def touch_moved(self, touch):
        # if the touch is in the "bubble" then
        if touch.location in self.layer.frame:
            self.current = touch.location

            # Set up a new frame based on latest touch location
            new_frame = Rect(self.current.x- 64, self.current.y - 64, 128, 128)
            self.layer.animate('frame', new_frame,0.01)

            # Calculate the relative x, y distance from center
            deltaX = (self.current.x - self.size.w/2.)/(self.size.w/2.-64)*100
            deltaY = (self.current.y - self.size.h/2.)/(self.size.h/2.-64)*100

            # round to nearest integer
            deltaX = int(deltaX)
            deltaY = int(deltaY)

            # and limit to between -100 and 100
            deltaX = max(min(100,deltaX),-100)
            deltaY = max(min(100,deltaY),-100)

            # The velocity is proportional to offset from center of screen
            self.velocity.x = deltaX
            self.velocity.y = deltaY


            # Various debugging print statements
            #velocity = sqrt((deltaX)**2 + (deltaY)**2)
            #angle = math.atan2(deltaY, deltaX)
            #print('Velocity = ' + str(round(velocity,2)) + ' at ' + str(round(angle * 180/math.pi, 2)) + 'deg.')
            #print('Moved to: ' + str(touch.location.x) + ', ' + str(touch.location.y))
            #print('Delta:    ' + str(deltaX) + ', ' + str(deltaY))
            #print('Sample Time: ' + str(self.dt) + 's')

            # print('Velocity = ' + str(self.velocity.x) + ', ' + str(self.velocity.y))

    def touch_ended(self, touch):
        # if the touch ends, immediately reset the velocities to 0
        self.velocity.x, self.velocity.y = 0, 0

        # debugging print
        #print('Velocity = ' + str(int(self.velocity.x)) + ', ' + str(int(self.velocity.y)))

        new_frame = Rect(self.size.w*0.5 - 64, self.size.h*0.5 - 64, 128, 128)
        self.layer.animate('frame', new_frame)

    def stop(self): # called when x is pressed to close
        #print 'Shutting down...\n'
        #self.server.shutdown()
        self.receive_broadcast = False
        #self.broadcast_thread.join(2)
        #self.s.shutdown(socket.SHUT_RDWR)
        #self.s.close()

if __name__ == '__main__':
    gui = MyScene()
    run(gui)

