import random
from midiutil.MidiFile import MIDIFile
import os


# Determines what number the next track should have based on the ones already present in the directory
currentTracks = os.listdir("tracks/")
num = 0
for i in range(0, len(currentTracks) + 1):
    num = i
    if f"track{num}.mid" not in currentTracks:
        break


# Lists the possibles pitches for the track from [36, 72] (C1 to C4) (removes half notes from the pitches)
half_notes = [37, 39, 42, 44, 46, 49, 51, 54, 56, 58, 61, 63, 66, 68, 70]
pitches = [x for x in list(range(36, 73)) if x not in half_notes]

# Creates the basic attributes for the midi file
mf = MIDIFile(1)
track = 0
time = 2
tempo = 56
mf.addTrackName(track, 0, f"track{num}")
mf.addTempo(track, time, tempo)
channel = 0
volume = 100
time_between_notes = [2, 10]  # The interval of time which can pass between 2 notes (both included)
num_notes = 50


# Clamps the given value to a certain range
def clamp(val, min_val, max_val):
    return max(min_val, min(max_val, val))


# Chooses a random value in a bell curve distribution such that the notes in the middle are
# much more likely to be chosen than the ones on the far ends of the keyboard
def randomInBellCurve(mean, st_deviation, min_val, max_val):
    return clamp(int(random.normalvariate(mean, st_deviation)), min_val, max_val)


# Adds a random note on the keyboard to be added to the midi file.
# The duration of the note is random (1s to 4s) and the time between each note is random too (2s to 10s).
def addNote():
    global time
    # Chooses if a chord will be played instead of a single note
    chord = True if random.random() > 0.7 else False

    duration = random.randint(1, 4)
    """ Unweighted choise of pitch for the note
    if chord:
        pitch_index = random.randint(2, len(pitches) - 3)
        pitch = [pitches[pitch_index - 2], pitches[pitch_index], pitches[pitch_index + 2]]

        mf.addNote(track, channel, pitch[0], time, duration, volume)
        mf.addNote(track, channel, pitch[1], time, duration, volume)
        mf.addNote(track, channel, pitch[2], time, duration, volume)
    else:
        pitch = random.choice(pitches)
        mf.addNote(track, channel, pitch, time, duration, volume)
    """

    # If a chord is to be played, choose a random full note and then play it with the 2 full notes
    # that are at a distance of 2 from the chosen note
    if chord:
        pitch_index = randomInBellCurve(11, 5, 2, len(pitches) - 3)
        pitch = [pitches[pitch_index - 2], pitches[pitch_index], pitches[pitch_index + 2]]

        mf.addNote(track, channel, pitch[0], time, duration, volume)
        mf.addNote(track, channel, pitch[1], time, duration, volume)
        mf.addNote(track, channel, pitch[2], time, duration, volume)
    else:  # If a single note is played, choses a random full note and adds it
        pitch_index = randomInBellCurve(11, 5, 0, len(pitches) - 1)
        mf.addNote(track, channel, pitches[pitch_index], time, duration, volume)

    time = time + duration + random.randint(time_between_notes[0], time_between_notes[1])


# Adds the number of random notes which is specified by num_notes to the midi file
for i in range(num_notes):
    addNote()

# Create the midi file and write the notes to it
with open(f"tracks/track{num}.mid", 'wb') as outf:
    mf.writeFile(outf)
