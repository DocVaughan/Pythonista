import console
import datetime
import logging
import paho.mqtt.client as mqtt
import socket
import sound
import time
import ui

class MyView (ui.View):
    def __init__(self):
        # This will also be called without arguments when the view is loaded from a UI file.
        # You don't have to call super. Note that this is called *before* the attributes
        # defined in the UI file are set. Implement `did_load` to customize a view after
        # it's been fully loaded from a UI file.

        # time used in calculation of wheb to send data
        self.last_time = 0.0

    def did_load(self):
        # This will be called when a view has been fully loaded from a UI file.
        pass


    def will_close(self):
        # This will be called when a presented view is about to be dismissed.
        # You might want to save data here.
        pass

    def draw(self):
        # This will be called whenever the view's content needs to be drawn.
        # You can use any of the ui module's drawing functions here to render
        # content into the view's visible rectangle.
        # Do not call this method directly, instead, if you need your view
        # to redraw its content, call set_needs_display().
        pass

    def layout(self):
        # This will be called when a view is resized. You should typically set the
        # frames of the view's subviews here, if your layout requirements cannot
        # be fulfilled with the standard auto-resizing (flex) attribute.
        pass

    def touch_began(self, touch):
        # Called when a touch begins.
        logger.debug('New touch at : {}'.format(touch.location))

    def touch_moved(self, touch):
        # Called when a touch moves.
        pass

    def touch_ended(self, touch):
        # Called when a touch ends
        logger.debug(' Touch ended')

    def keyboard_frame_will_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass

    def keyboard_frame_did_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.debug('Connected with result code {}'.format(rc))
    v['connectionStatus'].background_color = 'green'

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(v['subTopicText'].text)

# The callback for when the client disconnects from the server
def on_disconnect(client, userdata, rc):
    logger.debug('Disconnected...')
    v['connectionStatus'].background_color = 'red'

def on_message(client, userdata, msg):
    v['receivedText'].text = 'Topic: ' + msg.topic + '\nData: ' + msg.payload.decode(encoding='UTF-8') + '\n\n' + v['receivedText'].text
    logger.debug('Received Topic: ' + msg.topic + 'Data: ' + msg.payload.decode(encoding='UTF-8'))

def send_once(sender):

    if connected:
        pubTopic = v['pubTopicText'].text
        pubMessage = v['pubMessage'].text

        client.will_set(pubTopic)
        client.publish(pubTopic, pubMessage.encode('utf-8'), qos=0)

        logger.debug('Sending: {} once to {}:{} Topic {}'.format(pubMessage, broker, port, pubTopic))
    else:
        console.alert('Please Connect', 'Please connect to a broker before sending a message.', 'Ok', hide_cancel_button=True)

def change_subTopic(sender):
    global subTopic

    # unsubscribe from the old topic
    client.unsubscribe(subTopic)

    # then subscribe to the new one
    subTopic = v['subTopicText'].text
    client.subscribe(v['subTopicText'].text)

def toggle_connection(sender):
    global connected
    global client

    if connected:
        client.loop_stop()
        client.disconnect()
        connected = False
        v['connectionToggle'].title = 'Connect'
    else:
        # Set up callback functions for connect and disconnect
        # We'll use to trigger the status "LED"
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.will_set(pubTopic, payload='Pythonista disconnected...')

        # Attempt to connect to the broker, with a 60 sec timeout
        client.connect(broker, port, 60)

        client.loop_start()

        connected = True
        v['connectionToggle'].title = 'Disconnect'

if __name__ == '__main__':
    v = ui.load_view()

    if min(ui.get_screen_size()) >= 768:
        # iPad
        v.frame = (0, 0, 375, 600) # ~iPhone 6S size, minus titlebar
        v.present('sheet')
    else:
        # iPhone
        v.present()

    # TODO: Figure out while this doens't produce a debug log
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    v['subTopicText'].action = change_subTopic

    connected = False
    client = mqtt.Client() #client_id="DocV_Pythonista")
    # set up brocker socket - IP address and socket to send to
    broker, port = v['ipText'].text, int(v['portText'].text)
    pubTopic = v['pubTopicText'].text
    subTopic = v['subTopicText'].text

    # TODO: Implement password protected broker
    # if USERNAME is not None:
    #    client.username_pw_set(USERNAME, PASSWORD)

    last_time = time.time()
    sampling_time = float(v['sampleText'].text)


    while v.on_screen:
        if v['transmitSwitch'].value:
            if connected:
                if (time.time() - last_time > sampling_time):
                    sampling_time = float(v['sampleText'].text)
                    broker, port = v['ipText'].text, int(v['portText'].text)
                    pubTopic = v['pubTopicText'].text
                    pubMessage = v['pubMessage'].text
                    subTopic = v['subTopicText'].text

                    # client.will_set(pubTopic)
                    client.publish(pubTopic, pubMessage.encode('utf-8'), qos=0)

                    logger.debug('Sending: {} to {}:{} Topic {}'.format(pubMessage, broker, port, pubTopic))

                    last_time = time.time()
            else:
                v['transmitSwitch'].value = False
                console.alert('Please Connect', 'Please connect to a broker before sending a message.', 'Ok', hide_cancel_button=True)

    else:
        logger.debug('Closing...')
        client.disconnect()
        client.loop_stop()

