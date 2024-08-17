from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.harmony import Chord
from microtonal.players import Band, TonalPlayer, RythmicPlayer, Pattern
from microtonal.repl import App

app = App(
    band = Band(),
    tempo = 3,
)

drum_patterns = [
    Pattern(
        8,
        [(0,1), (1,1), (1.5,1), (3,1), (5,1), (6.5,1), (7,1)],
        [[0],   [1],   [0],     [1],   [1],   [0],     [1]],
    ),
    Pattern(
        8,
        [(0,1), (1,1), (1.5,1), (2,1), (3,1), (4,1), (4.5,1), (5,1), (6,1), (6.5,1), (7,1)],
        [[0,2], [1,2], [0],     [2],   [1,2], [2],   [0],     [1,2], [0,2], [0],     [1,2]],
    ),
]
organ_patterns = [
    Pattern(8, [(0, 6), (6, 2)], [[-3, 0, 2], [-1, 1, 4]]),
    # Pattern(8, [(0, 3), (3, 1)], [[0, 2, 4], [0, 3, 5]]),
]

app.band["drummer"] = RythmicPlayer(
    100, drum_patterns[0],
    [PercussiveInstrument.AcousticBassDrum, PercussiveInstrument.AcousticSnare, PercussiveInstrument.RideCymbal1],
)
app.band["organ"] = TonalPlayer(
    100, organ_patterns[0],
    300 * (Chord.I + 3/2 * Chord.I + 4/3 * Chord.I), MelodicInstrument.PercussiveOrgan,
)

# # test:
# app.band.play(3)

def change_drum_pattern(p: str):
    app.band["drummer"].pattern = drum_patterns[int(p)]

app.handlers["d"] = change_drum_pattern

app.start()
