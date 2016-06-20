# coding: utf-8
import matplotlib.pyplot as plt

with plt.xkcd():
	# Based on "The Data So Far" from XKCD by Randall Monroe
	# http://xkcd.com/373/
	fig = plt.figure()
	ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
	ax.bar([-0.125, 1.0-0.125], [0, 100], 0.25)
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	ax.xaxis.set_ticks_position('bottom')
	ax.set_xticks([0, 1])
	ax.set_xlim([-0.5, 1.5])
	ax.set_ylim([0, 110])
	ax.set_xticklabels(['CONFIRMED BY\nEXPERIMENT', 'REFUTED BY\nEXPERIMENT'])
	plt.yticks([])

	plt.title("CLAIMS OF SUPERNATURAL POWERS")

	fig.text(
	0.5, 0.05,
	'"The Data So Far" from xkcd by Randall Monroe',
	ha='center')

plt.show()