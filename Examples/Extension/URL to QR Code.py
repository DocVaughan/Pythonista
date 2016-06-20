# coding: utf-8

import qrcode
import appex

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	url = appex.get_url()
	if not url:
		print('No input URL found.')
		return
	print(url)
	img = qrcode.make(url)
	img.show()
	
if __name__ == '__main__':
	main()
