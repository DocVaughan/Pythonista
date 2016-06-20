#!python3

import ui
import appex
from random import randint
import console

# Map numbers to unicode dice symbols:
faces = {1: '\u2680', 2: '\u2681', 3: '\u2682',
         4: '\u2683', 5: '\u2684', 6: '\u2685'}

def make_widget_view():
	label = ui.Label(frame=(0, 0, 320, 64))
	label.name = 'Dice'
	label.text_color = 'white'
	label.font = ('<System>', 40)
	label.alignment = ui.ALIGN_CENTER
	return label

def main():
	if appex.is_widget():
		console.clear()
		label = appex.get_widget_view()
		# Check if the label already exists, if not, create it,
		# and set it as the widget's view.
		if not label or label.name != 'Dice':
			label = make_widget_view()
		appex.set_widget_view(label)
	else:
		label = make_widget_view()
		label.background_color = '#333'
		label.name = 'Widget Preview'
		label.present('sheet')
	# Roll two dice.
	a, b = randint(1, 6), randint(1, 6)
	# Update the label's text
	label.text = faces[a] + ' ' + faces[b]

if __name__ == '__main__':
	main()
