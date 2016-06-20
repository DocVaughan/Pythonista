# coding: utf-8

'''Simple demo of using UIScreen to get/set the screen brightness'''

from objc_util import *
UIScreen = ObjCClass('UIScreen')

# If the current screen brightness is set to less than 30%, it is set to 60% ("day mode", otherwise set it to 10% ("night mode").
	
def main():
	screen = UIScreen.mainScreen()
	if screen.brightness() < 0.3:
		screen.setBrightness_(0.6)
	else:
		screen.setBrightness_(0.1)

if __name__ == '__main__':
	main()