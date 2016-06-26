import datetime
import logging
import paho.mqtt.client as mqtt
import socket
import sound
import time
import ui


# TODO: Figure out while this doens't produce a debug log
logger = logging.getLogger('MQTT joystick UI ')
logger.setLevel(logging.DEBUG)

VERT_OFFSET = 0

def change_alpha(sender):
    def animation():
        v['out_y'].alpha = v['transmitSwitch'].value
        v['out_x'].alpha = v['transmitSwitch'].value
        v['sending_label'].alpha = v['transmitSwitch'].value
    ui.animate(animation, duration=1.0)


class MyView (ui.View):
    def __init__(self):
        # This will also be called without arguments when the view is loaded from a UI file.
        # You don't have to call super. Note that this is called *before* the attributes
        # defined in the UI file are set. Implement `did_load` to customize a view after
        # it's been fully loaded from a UI file.

        # both desired velocities are initially zero
        self.velocity = (0, 0)
        
        # Define the joystick image
        self.joy_img = ui.Image.named('emj:White_Circle')
        
        # Define how often to send data
        self.SAMPLING_TIME = 0.1
        
        # time used in calculation of wheb to send data
        self.last_time = 0.0

    def did_load(self):
        # This will be called when a view has been fully loaded from a UI file.
        self.current = (self.width/2, self.height/2-VERT_OFFSET)
        
        self['out_y'].alpha = 0.0 
        self['out_x'].alpha = 0.0
        self['sending_label'].alpha = 0.0
        self['settingsView'].hidden = True
        


    def will_close(self):
        # This will be called when a presented view is about to be dismissed.
        # You might want to save data here.
        self.velocity = (0, 0)

    def draw(self):
        # This will be called whenever the view's content needs to be drawn.
        # You can use any of the ui module's drawing functions here to render
        # content into the view's visible rectangle.
        # Do not call this method directly, instead, if you need your view
        # to redraw its content, call set_needs_display().
        
        # border = ui.Path.rect(self.center.x-44, self.center.y-88, 88, 88)
        # ui.set_color('red')
        # border.fill()

        self.joy_img.draw(self.current[0]-44, self.current[1]-44, 88, 88)
        
        v['out_x'].text = str(self.velocity[0])
        v['out_y'].text = str(self.velocity[1])

    def layout(self):
        # This will be called when a view is resized. You should typically set the
        # frames of the view's subviews here, if your layout requirements cannot
        # be fulfilled with the standard auto-resizing (flex) attribute.
        self.current = (self.width/2, self.height/2-VERT_OFFSET)
        self.velocity = (0, 0)
        v.set_needs_display()

    def touch_began(self, touch):
        # Called when a touch begins.
        
        logger.debug('New touch at : {}'.format(touch.location))

        # if the touch is in the "bubble" then
        if touch.location in ui.Rect(self.center.x-44, self.center.y-88-VERT_OFFSET, 88, 88):
            sound.play_effect('Coin_3')
            self.current = touch.location
            self.initial = touch.location
            self.move_okay = True
        else:
            sound.play_effect('Error')
            time.sleep(0.25)
            sound.play_effect('Error')
            self.move_okay = False

    def touch_moved(self, touch):
        # Called when a touch moves.
        if self.move_okay:
            self.current = touch.location
                    
            # Calculate the relative x, y distance from center
            deltaX = (self.current.x - self.initial.x)
            deltaY = -(self.current.y - self.initial.y)
            
            deltaX = (self.current.x - self.width/2) / (self.width/2 - 88) * 100.0
            
            deltaY = -(self.current.y - self.height/2) / (self.height/2 - 88) * 100.0
    
            # round to nearest integer
            deltaX = int(deltaX)
            deltaY = int(deltaY)
    
            # and limit to between -100 and 100
            deltaX = max(min(100,deltaX),-100)
            deltaY = max(min(100,deltaY),-100)
            
            self.velocity = (deltaX, deltaY)
            logger.debug(' Current velocity: {}'.format(self.velocity))
    
            v.set_needs_display()

    def touch_ended(self, touch):
        # Called when a touch ends
        logger.debug(' Touch ended')
        
        # if the touch ends, immediately reset the velocities to 0
        if self.move_okay:
            self.current.x, self.current.y = self.width/2, self.height/2-VERT_OFFSET
            self.velocity = (0, 0)
            v.set_needs_display()

    def keyboard_frame_will_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass

    def keyboard_frame_did_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass
        
class settingsView (ui.View):
    def __init__(self):
        pass
        
def open_settings(sender):
    def animation():
        v['settingsView'].hidden = False
        # Stop Sending while we're changing settings
        v['transmitSwitch'].value = 0
        v['transmitSwitch'].enabled = False
        
        v['out_y'].alpha = v['transmitSwitch'].value
        v['out_x'].alpha = v['transmitSwitch'].value
        v['sending_label'].alpha = v['transmitSwitch'].value

    ui.animate(animation, duration=1.0)

def close_settings(sender):
    v['settingsView'].hidden = True
    v['transmitSwitch'].enabled = True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.debug('Connected with result code {}'.format(rc))
    v['connectionStatus'].background_color = 'green'
    #v['connectionStatus'].text = 'green'

# The callback for when the client disconnects from the server
def on_disconnect(client, userdata, rc):
    logger.debug('Disconnected...')
    v['connectionStatus'].background_color = 'red'

if __name__ == '__main__':
    v = ui.load_view()
    v.present('sheet')
    
    last_time = time.time()
    sampling_time = float(v['settingsView']['sampleText'].text)

    # set up brocker socket - IP address and socket to send to
    broker, port = v['settingsView']['ipText'].text, int(v['settingsView']['portText'].text)
    topic = v['settingsView']['topicText'].text
    
    client = mqtt.Client(client_id="DocV_Pythonista")

    # TODO: Implement password protected broker
    # if USERNAME is not None:
    #    client.username_pw_set(USERNAME, PASSWORD)
    
    # Set up callback functions for connect and disconnect
    # We'll use to trigger the status "LED"
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.will_set(topic, payload='Pythonista disconnected...')
    client.loop_start()

    # Attempt to connect to the broker, with a 60 sec timeout
    client.connect(broker, port, 60)
    
    while v.on_screen:
        data = '{}, {}'.format(v.velocity[0], v.velocity[1])

        if v['transmitSwitch'].value:
            if (time.time() - last_time > sampling_time):
                sampling_time = float(v['settingsView']['sampleText'].text)
                broker, port = v['settingsView']['ipText'].text, int(v['settingsView']['portText'].text)
                topic = v['settingsView']['topicText'].text
                
                
                client.will_set(topic)
                client.publish(topic, data.encode('utf-8'), qos=0)
                
                logger.debug(' Sending: {} to {}:{} Topic {}'.format(data, broker, port, topic))
                # print(' Sending: {} to {}:{}'.format(data, host, port))
           
                last_time = time.time()
    else:
        logger.debug('Closing...')
        client.disconnect()
        client.loop_stop()
