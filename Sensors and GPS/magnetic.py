import motion
import time
import numpy as np

motion.start_updates()
time.sleep(2)
while True:
    mag_data = motion.get_magnetic_field()
    heading = (360.0 - np.arctan2(mag_data[1], mag_data[0]) * 180.0/np.pi) % 360 
    
    if mag_data[3] != -1:
        break
        
    # print 'Please calibrate the compass by moving the device...'
    time.sleep(0.5)


print('\r\nMagnetometer successfully calibrated...')
print('Data:    \t {}'.format(motion.get_magnetic_field()))
print('Heading: \t {:5.2f}'.format(heading))
    


motion.stop_updates()
