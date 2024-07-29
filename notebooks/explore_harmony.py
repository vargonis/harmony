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

#%%
play_chord(300, [1, 7/6, 4/3], Program.PercussiveOrgan, 100, 1)
play_chord(400, [1, 8/7, 4/3], Program.PercussiveOrgan, 100, 1)


#%%
base = 200
play_arpeggio(base, [1, 7/6, 4/3, 3/2, 7/4, 2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 7/6, 4/3, 3/2, 7/4, 2], Program.YamahaGrandPiano, 127, .7)

play_arpeggio(base, [1, 9/8, 7/6, 6/5, 5/4, 4/3, 3/2, 8/5, 7/4, 16/9, 15/8, 2], Program.Fiddle, 127, .5)
play_arpeggio(base, [1, 9/8, 7/6, 5/4, 4/3, 3/2, 8/5, 7/4, 15/8, 2], Program.Fiddle, 127, .5)

play_arpeggio(base, [1, 7/6, 9/7, 4/3, 3/2, 7/4, 2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 7/6, 9/7, 3/2, 12/7, 2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 8/7, 9/7, 3/2, 12/7, 2], Program.Fiddle, 127, .7)

play_arpeggio(base, [1, 8/9, 4/5, 3/2, 7/4, 2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 8/9, 4/5, 2/3, 4/7, 1/2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 9/8, 5/4, 3/2, 7/4, 2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 10/9, 5/4, 3/2, 7/4, 2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 10/9, 5/4, 3/2, 12/7, 2], Program.Fiddle, 127, .7)
play_arpeggio(base, [1, 10/9, 5/4, 3/2, 17/7, 2], Program.Fiddle, 127, .7)

play_arpeggio(base, [1, 10/9, 5/4, 3/2, 17/7, 2], Program.BowedGlass, 127, .7)