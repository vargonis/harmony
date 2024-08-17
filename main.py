from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.harmony import Chord
from microtonal.patterns import Note, Pattern, S, T, W
from microtonal.players import Band, TonalPlayer, RythmicPlayer
from microtonal.repl import App

app = App(
    band = Band(),
    tempo = 3,
)

kit = [PercussiveInstrument.AcousticBassDrum, PercussiveInstrument.AcousticSnare, PercussiveInstrument.RideCymbal1]
b, s, r = Note(0, 1, 0), Note(0, 1, 1), Note(0, 1, 2)
snare = Pattern(2, T(1) * s)
drum_1 = Pattern(8, b + T(1.5) * b + T(6.5) * b)
drum_2 = Pattern(8, b + T(1.5) * b + T(4.5) * b + T(6) * b + T(6.5) * b)
ride = Pattern(1, r)
drum_patterns = [drum_1 + snare**4, drum_2 + snare**4 + ride**8]

mode = 300 * (Chord.I + 3/2 * Chord.I + 4/3 * Chord.I)
n = Note(0, 1, 0)
organ_patterns = [
    Pattern(6, W(6) * (S(-3) * n + n + S(2) * n)) * Pattern(2, W(2) * (S(-1) * n + S(1) * n  + S(4) * n))
]

app.band["drummer"] = RythmicPlayer(100, drum_patterns[0], kit)
app.band["organ"] = TonalPlayer(100, organ_patterns[0], mode, MelodicInstrument.PercussiveOrgan)

# # test:
# app.band.play(3)

def change_drum_pattern(p: str):
    app.band["drummer"].pattern = drum_patterns[int(p)]

app.handlers["d"] = change_drum_pattern

app.start()
