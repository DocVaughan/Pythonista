#! python2

# NOTE: The first line in this script specifies that it should always be run using Python 2.7.
# The `midiutil` module is currently not available for Python 3.

'''Generates a MIDI file with 12 random notes in C major, using the midiutil module. The instrument is also picked randomly. The result is then played with the sound.MIDIPlayer class.
If nothing happens, make sure that your device isn't muted.
'''

from midiutil.MidiFile import MIDIFile
from random import choice, randint
import sound

# Configure a MIDI file with one track:
midi = MIDIFile(1)
midi.addTempo(0, 0, 180)

# Select a random instrument:
program = randint(0, 255)
midi.addProgramChange(0, 0, 0, program)

# Generate some random notes:
duration = 1
c_major = [60, 62, 64, 65, 67, 69, 71]
for t in range(12):
	pitch = choice(c_major)
	# track, channel, pitch, time, duration, volume
	midi.addNote(0, 0, pitch, t * duration, duration, 100)
	
# Write output file:
with open('output.mid', 'w') as f:
	midi.writeFile(f)

# Play the result:
player = sound.MIDIPlayer('output.mid')
player.play()