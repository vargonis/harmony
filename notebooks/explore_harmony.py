import time
from microtonal import Synth, Program, GreekChord, GreekScale

synth = Synth()


def play_chord(program, base, chord, velocity, duration):
    note_ids = synth.chord_on(program, base, chord, velocity)
    time.sleep(duration)
    synth.chord_off(note_ids)

def play_scale(program, base, scale, velocity, duration):
    freq = base
    i = synth.note_on(program, freq, velocity)
    time.sleep(duration)
    synth.note_off(i)
    for x in scale:
        freq *= x
        i = synth.note_on(program, freq, velocity)
        time.sleep(duration)
        synth.note_off(i)

def play_arpeggio(program, base, chord, velocity, duration):
    for x in chord:
        i = synth.note_on(program, base * x, velocity)
        time.sleep(duration)
        synth.note_off(i)

#%%
play_chord(Program.PercussiveOrgan, 300, [1, 7/6, 4/3], 100, 1)
play_chord(Program.PercussiveOrgan, 400, [1, 8/7, 4/3], 100, 1)


for _ in range(3):
    play_chord(Program.PercussiveOrgan, 300, [1, 7/6, 4/3], 100, 1)
    play_chord(Program.PercussiveOrgan, 300, [1, 3/2, 7/4], 100, 1)

for _ in range(3):
    play_chord(Program.PercussiveOrgan, 300, [1/2, 7/6, 4/3], 100, 1)
    play_chord(Program.PercussiveOrgan, 300, [1/2, 7/8, 3/2], 100, 1)


import numpy as np

play_chord(Program.PercussiveOrgan, 300, [1, 7/6, 4/3], 100, 1)
play_chord(Program.PercussiveOrgan, 300, 4/3 * np.array([1, 7/6, 4/3]), 100, 1)
play_chord(Program.PercussiveOrgan, 300, [3/2, 7/4, 2], 100, 1)
play_chord(Program.PercussiveOrgan, 300, [1, 7/6, 4/3], 100, 1)

play_chord(Program.PercussiveOrgan, 300, np.array([1, 7/6, 4/3]), 100, 1)
play_chord(Program.PercussiveOrgan, 300, 5/4 * np.array([1, 7/6, 4/3]), 100, 1)
play_chord(Program.PercussiveOrgan, 300, 4/3 * np.array([1, 7/6, 4/3]), 100, 1)
play_chord(Program.PercussiveOrgan, 300, GreekChord.MAJOR, 100, 1)


#%%
base = 200
play_arpeggio(Program.Fiddle, base, [1, 7/6, 4/3, 3/2, 7/4, 2], 127, .7)
play_arpeggio(Program.YamahaGrandPiano, base, [1, 7/6, 4/3, 3/2, 7/4, 2], 127, .7)

play_arpeggio(Program.Fiddle, base, [1, 9/8, 7/6, 6/5, 5/4, 4/3, 3/2, 8/5, 7/4, 16/9, 15/8, 2], 127, .5)
play_arpeggio(Program.Fiddle, base, [1, 9/8, 7/6, 5/4, 4/3, 3/2, 8/5, 7/4, 15/8, 2], 127, .5)

play_arpeggio(Program.Fiddle, base, [1, 7/6, 9/7, 4/3, 3/2, 7/4, 2], 127, .7)
play_arpeggio(Program.Fiddle, base, [1, 7/6, 9/7, 3/2, 12/7, 2], 127, .7)
play_arpeggio(Program.Fiddle, base, [1, 8/7, 9/7, 3/2, 12/7, 2], 127, .7)

play_arpeggio(Program.Fiddle, base, [1, 8/9, 4/5, 3/2, 7/4, 2], 127, .7)
play_arpeggio(Program.Fiddle, base, [1, 8/9, 4/5, 2/3, 4/7, 1/2], 127, .7)
play_arpeggio(Program.Fiddle, base, [1, 9/8, 5/4, 3/2, 7/4, 2], 127, .7)
play_arpeggio(Program.Fiddle, base, [1, 10/9, 5/4, 3/2, 7/4, 2], 127, .7)
play_arpeggio(Program.Fiddle, base, [1, 10/9, 5/4, 3/2, 12/7, 2], 127, .7)
play_arpeggio(Program.Fiddle, base, [1, 10/9, 5/4, 3/2, 17/7, 2], 127, .7)

play_arpeggio(Program.BowedGlass, base, [1, 10/9, 5/4, 3/2, 17/7, 2], 127, .7)