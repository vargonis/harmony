from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.harmony import Chord
from microtonal.patterns import Pattern, s, T, W
from microtonal.players import Band, TonalPlayer, RythmicPlayer
from microtonal.repl import App

app = App(
    band = Band(),
    n_beats = 8,
    tempo = .4,
)

kit = [PercussiveInstrument.AcousticBassDrum, PercussiveInstrument.AcousticSnare, PercussiveInstrument.RideCymbal1]
snare = Pattern(2, T(1) * s(1))
drum_1 = Pattern(8, (T(0) + T(1.5) + T(6.5)) * s(0))
drum_2 = Pattern(8, (T(0) + T(1.5) + T(4.5) + T(6) + T(6.5)) * s(0))
ride = Pattern(1, s(2))
drum_patterns = [
    drum_1 + snare**4,
    drum_2 + snare**4 + ride**8,
]

base = 300 #  * (Chord.I + 3/2 * Chord.I + 4/3 * Chord.I)
organ_patterns = [
    Pattern(6, W(6) * base * Chord.I**-1) * Pattern(2, W(2) * (3/4 * base) * Chord.I**1)
]

app.band["drummer"] = RythmicPlayer(100, drum_patterns[0], kit)
app.band["organ"] = TonalPlayer(100, organ_patterns[0], MelodicInstrument.PercussiveOrgan)

# test:
app.band.play("drummer", .4)

def change_drum_pattern(p: str):
    app.band["drummer"].pattern = drum_patterns[int(p)]

app.handlers["d"] = change_drum_pattern

app.start()


#%%
from random import randint

mode = 300 * (
    Chord.II + # 4/3 * Chord.II + # 16/9 * Chord.II + 
    3/4 * Chord.II # + 9/16 * Chord.II
)
def rand_pattern():
    return Pattern(8, [T(i) * s(mode[randint(-6, 6)]) for i in range(8)])
patterns = [rand_pattern() for _ in range(3)]

app.band["bed"] = TonalPlayer(80, Pattern(6, W(6) * 300 * Chord.II) * Pattern(2, W(2) * (3/4) * 300 * Chord.II), MelodicInstrument.AhhChoir)
app.band["melody"] = TonalPlayer(110, patterns[1], MelodicInstrument.Clarinet)

# test:
app.band["melody"].pattern = patterns[2]
app.band.play(.4)
app.start()

#%%
c = 8/9
b1 = Pattern(4, W(4) * 300 * Chord.Im)
b2 = Pattern(4, W(4) * 300 * Chord.II)
b3 = Pattern(4, W(4) * 300 * c * Chord.I)
b4 = Pattern(4, W(4) * 300 * c * Chord.IIm)
b5 = Pattern(4, W(4) * 300 * c**2 * Chord.Im)
b6 = Pattern(4, W(4) * 300 * c**2 * Chord.II)
b7 = Pattern(4, W(4) * 300 * c**3 * Chord.I)
b8 = Pattern(4, W(4) * 300 * c * Chord.II)

app = App(
    band = Band(),
    n_beats = 4 * 8,
    tempo = .4,
)
app.band["bed"] = TonalPlayer(80, b1 * b2 * b3 * b4 * b5 * b6 * b7 * b8, MelodicInstrument.AhhChoir)

app.start()


