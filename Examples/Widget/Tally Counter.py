#!python3

import ui
import appex
import console
import sound

counter = 0
# Try to load previous counter value from file:
try:
	with open('.TallyCounter.txt') as f:
		counter = int(f.read())
except IOError:
	pass

def button_tapped(sender):
	# Update the counter, depending on which button was tapped:
	global counter
	if sender.name == 'plus':
		counter += 1
		sound.play_effect('ui:click1')
	elif sender.name == 'minus':
		counter = max(0, counter - 1)
		sound.play_effect('ui:click2')
	elif sender.name == 'reset':
		counter = 0
		sound.play_effect('ui:switch34')
	# Update the label:
	sender.superview['text_label'].text = str(counter)
	# Save the new counter value to a file:
	with open('.TallyCounter.txt', 'w') as f:
		f.write(str(counter))

def make_widget_view():
	v = ui.View(frame=(0, 0, 320, 64))
	label = ui.Label(frame=(0, 0, 320-44, 64))
	label.name = 'text_label'
	label.flex = 'WH'
	label.text_color = 'white'
	label.font = ('<System>', 48)
	label.alignment = ui.ALIGN_CENTER
	label.text = str(counter)
	v.add_subview(label)
	minus_btn = ui.Button()
	minus_btn.frame = (320-128, 0, 64, 64)
	minus_btn.image = ui.Image.named('iow:minus_circled_32')
	minus_btn.name = 'minus'
	plus_btn = ui.Button()
	plus_btn.frame = (320-64, 0, 64, 64)
	plus_btn.image = ui.Image.named('iow:plus_circled_32')
	plus_btn.name = 'plus'
	for btn in (plus_btn, minus_btn):
		btn.flex = 'HL'
		btn.tint_color = 'white'
		btn.action = button_tapped
		v.add_subview(btn)
	reset_btn = ui.Button()
	reset_btn.frame = (0, 0, 64, 64)
	reset_btn.tint_color = 'white'
	reset_btn.image = ui.Image.named('iow:skip_backward_32')
	reset_btn.name = 'reset'
	reset_btn.action = button_tapped
	v.add_subview(reset_btn)
	v.name = 'TallyCounter'
	return v

def main():
	if appex.is_widget():
		console.clear()
		v = appex.get_widget_view()
		# Check if the counter view already exists, if not, create it,
		# and set it as the widget's view.
		if not v or v.name != 'TallyCounter':
			v = make_widget_view()
			appex.set_widget_view(v)
	else:
		v = make_widget_view()
		v.name = 'Widget Preview'
		v.background_color = '#333'
		v.present('sheet')

if __name__ == '__main__':
	main()
	
