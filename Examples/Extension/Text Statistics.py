# coding: utf-8

import appex
from html2text import html2text
import console
import re

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	text = appex.get_text()
	if not text:
		print('No text input found.')
		return
	text = html2text(text)
	text = text.strip('* \n')
	words = text.split()
	sentences = [x for x in re.split(r'[\.?!]', text) if len(x) > 0]
	console.alert('Statistics', '%i words\n%i sentences\n%i characters' % (len(words), len(sentences), len(text)), 'OK', hide_cancel_button=True)

if __name__ == '__main__':
	main()
	