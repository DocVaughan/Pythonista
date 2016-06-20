from scene import *
import socket
import threading
import socketserver

data_recieved = ', , , '

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global data_recieved
        data = self.request[0].strip()
        socket = self.request[1]
        #string_to_print = "Velocity from {}: ".format(self.client_address[0]) + data

        data_recieved = data


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass




class MyScene (Scene):
    def setup(self):
        # This will be called before the first frame is drawn.
        # Set up the root layer and one other layer:
        self.root_layer = Layer(self.bounds)

        # variable for 'deadman switch' touch event
        self.deadmanTouch = False

        # initial velocity is zero in both directions
        self.velocity = Point(x = 0, y = 0)
        self.data_str = str(self.velocity.x) + ', ' + str(self.velocity.y)

        # Set up UDP - IP address and port to send to
        self.HOST, self.PORT = '10.0.1.19', 2390

        # SOCK_DGRAM is the socket type to use for UDP sockets
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        # set up the receiving thread
        # Port 0 means to select an arbitrary unused port
        HOST, PORT = "0.0.0.0", 2390

        self.server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
        ip, port = self.server.server_address

        # Start a thread with the server
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()
        # print "Server loop running in thread:", server_thread.name


        self.x = self.size.w * 0.5
        self.xdot = 0.0
        self.xddot = 0.0

        self.y = self.size.h * 0.5
        self.ydot = 0.0
        self.yddot = 0.0


        # set up bubble image
        self.layer = Layer(Rect(self.x - 64, self.y - 64, 128, 128))
        self.layer.image = 'White_Circle'
        self.root_layer.add_layer(self.layer)


    def draw(self):
        # if the user is touching the screen, update velocity based on tilt
        if self.deadmanTouch:
            backgroundColor = Color(0.75, 0.75, 0.75) #light gray
            kx = 1.2
            cx = 1.0
            ky = 1.0
            cy = 1.7

            g = gravity()
            #print(g)

            self.xddot = kx * (self.size.w * 0.5 - self.x) - cx * self.xdot + g.x * 500
            self.xdot += self.xddot * self.dt

            self.x += self.xdot * self.dt + self.xddot * self.dt**2


            self.yddot = ky * (self.size.h * 0.5 - self.y) - cy * self.ydot + g.y * 1000.
            self.ydot += self.yddot * self.dt

            self.y += self.ydot * self.dt + self.yddot * self.dt**2

            self.x = min(self.size.w - 64, max(64, self.x))
            self.y = min(self.size.h - 64, max(64, self.y))

            new_frame = Rect(self.x - 64, self.y - 64, 128, 128)

        else:
            backgroundColor = Color(0, 0, 0) #black
            self.x = self.size.w * 0.5
            self.y = self.size.h * 0.5
            new_image = 'White_Circle'
            new_frame = Rect(self.x - 64, self.y - 64, 128, 128)

        # calculate the velocity as a % of maximum displacement in x, y
        # Limit to integer values
        x_vel = int( 100 * (self.x - self.size.w/2.) / (self.size.w/2.-64) )
        y_vel = int( 100 * (self.y - self.size.h/2.) / (self.size.h/2.-64) )

        # make a string velocities as comma separated valued
        self.data_str = str(x_vel) + ', ' + str(y_vel)

        # send velocity as x, y pair string
        self.sock.sendto(self.data_str.encode('utf-8'), (self.HOST, self.PORT))

        # save velocity in the scene
        self.velocity.x, self.velocity.y = x_vel, y_vel

        # update the location of the bubble and change background color based on touch
        self.layer.animate('frame', new_frame, 0.1)
        self.root_layer.animate('background', backgroundColor, 0.1)

        # add a text layer to show the output
        screen_string= 'Output = ' + self.data_str
        text_layer = TextLayer(screen_string, 'Futura-Medium', 36)
        text_layer.frame.center(self.size.w/2.,50)
        self.add_layer(text_layer)

        # Draw the updates
        self.root_layer.update(self.dt)
        self.root_layer.draw()

        # A hack for now...
        #   remove the text layer in order to animate the changes next cycle
        text_layer.remove_layer()

        lat, lon, heading, speed = data_recieved.rsplit(', ')

        text('Lat: \nLong: \nSpeed: \nHeading:', font_name='SourceCodePro-Regular', font_size=20.0, x=5, y=5., alignment = 9)

        text(' ' + str(lat) + '\n' + str(lon) + '\n  ' + speed + '\n ' + heading, font_name='SourceCodePro-Regular', font_size=20.0, x=105, y=5., alignment = 9)


    def touch_began(self, touch):
        self.deadmanTouch = True


    def touch_moved(self, touch):
        pass


    def touch_ended(self, touch):
        self.deadmanTouch = False

    def stop(self): # called when x is pressed to close
        #print 'Shutting down...\n'
        self.server.shutdown()


if __name__ == '__main__':
    gui = MyScene()
    run(gui)

