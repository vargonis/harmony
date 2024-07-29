import time
from microtonal import Synth, Program, GreekChord, GreekScale

synth = Synth()


def play_chord(base, chord, program, velocity, duration):
    note_ids = synth.chord_on(base, chord, program, velocity)
    time.sleep(duration)
    synth.chord_off(note_ids)

def play_scale(base, scale, program, velocity, duration):
    freq = base
    i = synth.note_on(freq, program, velocity)
    time.sleep(duration)
    synth.note_off(i)
    for x in scale:
        freq *= x
        i = synth.note_on(freq, program, velocity)
        time.sleep(duration)
        synth.note_off(i)

def play_arpeggio(base, chord, program, velocity, duration):
    for x in chord:
        i = synth.note_on(base * x, program, velocity)
        time.sleep(duration)
        synth.note_off(i)

play_chord(300, GreekChord.MAJOR, Program.PercussiveOrgan, 100, 1)
play_chord(100, GreekChord.MINOR, Program.YamahaGrandPiano, 100, 1)
play_arpeggio(100, GreekChord.MINOR, Program.Dulcimer, 100, .5)

play_scale(100, GreekScale.MAJOR, Program.YamahaGrandPiano, 100, .1)
play_scale(100, GreekScale.MINOR, Program.YamahaGrandPiano, 100, .1)


#%%
# A slightly more complex example. By the way, we need to come up with a good way of interacting with the system,
# one that turns it into an "instrument"... This is intended as a preliminary exploration.

chord = synth.chord_on(300, GreekChord.MAJOR, Program.PercussiveOrgan, 90)
time.sleep(1)
play_scale(300, GreekScale.MAJOR, Program.YamahaGrandPiano, 127, .3)
time.sleep(1)
synth.chord_off(chord)

# Need at least a scheduler, see https://docs.python.org/3/library/sched.html, or a full event-driven application framework, like circuits https://circuits.readthedocs.io/en/latest/tutorials/woof/index.html.
# An event-driven approach should simplify having full control of what's happening, in real time.