# coding: utf-8

# NOTE: When you run this script, you will be prompted to allow access to your reminders. The script will (obviously) not work correctly if you deny this permission. You can change Pythonista's permissions from the Settings app.

import reminders

def main():
	todo = reminders.get_reminders(completed=False)
	print('TODO List\n=========')
	for r in todo:
		print('[ ] ' + r.title)
	done = reminders.get_reminders(completed=True)
	print('DONE\n====')
	for r in done:
		print('[x] ' + r.title)

if __name__ == '__main__':
	main()