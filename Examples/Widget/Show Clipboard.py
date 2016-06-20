#!python3

import ui
import appex
import clipboard
import console

def clear_button_tapped(sender):
	clipboard.set('')
	sender.superview['text_label'].text = 'Clipboard: (Empty)'

def make_widget_view():
	v = ui.View(frame=(0, 0, 320, 64))
	label = ui.Label(frame=(0, 0, 320-44, 64))
	label.name = 'text_label'
	label.flex = 'WH'
	label.text_color = 'white'
	label.font = ('<System>', 14)
	label.number_of_lines = 0
	v.add_subview(label)
	clear_btn = ui.Button()
	clear_btn.frame = (320-44, 0, 44, 64)
	clear_btn.image = ui.Image.named('iow:ios7_trash_32')
	clear_btn.flex = 'HL'
	clear_btn.tint_color = 'white'
	clear_btn.action = clear_button_tapped
	v.add_subview(clear_btn)
	v.name = 'Clipboard'
	return v
	
def main():
	if appex.is_widget():
		console.clear()
		v = appex.get_widget_view()
		# Check if the clipboard view already exists, if not, create it,
		# and set it as the widget's view.
		if not v or v.name != 'Clipboard':
			v = make_widget_view()
		appex.set_widget_view(v)
	else:
		v = make_widget_view()
		v.background_color = '#333'
		v.name = 'Widget Preview'
		v.present('sheet')
	v['text_label'].text = 'Clipboard: ' + (clipboard.get() or '(Empty)')

if __name__ == '__main__':
	main()
	
