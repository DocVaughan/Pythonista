#!python3

import ui
import appex
import math
import console

# Define launcher shortcuts that should appear in the widget,
# feel free to edit these:
shortcuts = [
	{'title': ' Google', 'url': 'http://google.com',
	'icon': 'iow:ios7_search_24'},
	{'title': ' StackOverflow', 'url': 'http://stackoverflow.com',
	'icon': 'iow:help_circled_24'},
	{'title': ' Forum', 'url': 'http://forum.omz-software.com',
	'icon': 'iow:ios7_chatbubble_24'},
	{'title': ' Pythonista', 'url': 'http://pythonista-app.com',
	'icon': 'iow:ios7_world_24'},
	{'title': ' Python.org', 'url': 'http://python.org',
	'icon': 'iow:ios7_world_24'},
	{'title': ' @olemoritz', 'url': 'http://twitter.com/olemoritz',
	'icon': 'iow:social_twitter_24'},
]

def button_tapped(sender):
	url = sender.name
	import webbrowser
	webbrowser.open(url)

def main():
	if not appex.is_widget():
		print('This script must be run in the Pythonista Today widget (in Notification Center). You can configure the widget script in the settings.')
		return
	console.clear()
	v = appex.get_widget_view()
	# If the shortcuts change, change the view name as well,
	# so it is reloaded.
	view_name = 'Launcher_' + str(shortcuts)
	# Check if the launcher view already exists, if not,
	# create it, and set it as the widget's view.
	if not v or v.name != view_name:
		h = math.ceil(len(shortcuts) / 3) * 44
		v = ui.View(frame=(0, 0, 300, h))
		# Create a button for each shortcut
		for i, s in enumerate(shortcuts):
			btn = ui.Button(title=s['title'])
			btn.image = ui.Image.named(s['icon'])
			btn.frame = ((i % 3) * 100, (i // 3) * 44, 100, 44)
			btn.flex = 'LRWH'
			btn.tint_color = 'white'
			# Just store the shortcut URL in the button's name attribute.
			# This makes it easy to retrieve it in the button_tapped action.
			btn.name = s['url']
			btn.action = button_tapped
			v.add_subview(btn)
		v.name = view_name
		appex.set_widget_view(v)

if __name__ == '__main__':
	main()
