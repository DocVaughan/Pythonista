# coding: utf-8

# NOTE: When you run this script, you will be prompted to allow access to your reminders. The script will (obviously) not work correctly if you deny this permission. You can change Pythonista's permissions from the Settings app.

import reminders
import dialogs
from datetime import datetime, timedelta

def main():
	title = dialogs.input_alert('Remind me in 5 minutes', 'Enter a title.', '', 'Remind me')
	r = reminders.Reminder()
	r.title = title
	due = datetime.now() + timedelta(minutes=5)
	r.due_date = due
	alarm = reminders.Alarm()
	alarm.date = due
	r.alarms = [alarm]
	r.save()
	dialogs.hud_alert('Reminder saved')

if __name__ == '__main__':
	main()