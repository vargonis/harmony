from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.harmony import ChordType
from microtonal.parts import Chord, Hit, Part, T
from microtonal.players import Band, TonalPlayer, RythmicPlayer
from microtonal.repl import App

app = App(
    band = Band(),
    tempo = .4,
)

d = Hit(0, 1, PercussiveInstrument.AcousticBassDrum)
s = Hit(0, 1, PercussiveInstrument.AcousticSnare)
r = Hit(0, 1, PercussiveInstrument.RideCymbal1)
snare = Part(2, T(1) * s)
drum_1 = Part(8, (T(0) + T(1.5) + T(6.5)) * d)
drum_2 = Part(8, (T(0) + T(1.5) + T(4.5) + T(6) + T(6.5)) * d)
ride = Part(1, r)
drums_parts = [
    drum_1 + snare**4,
    drum_2 + snare**4 + ride**8,
]

base = 300
tonic = Chord(0, 1, base * ChordType.I)
subdominant = Chord(0, 1, 3/4 * base * ChordType.I)
organ_parts = [
    Part(6, T(0,6) * tonic**-1) * Part(2, T(0,2) * subdominant**1)
    # Part(8, T(0,6) * tonic**-1 + T(6,2) * subdominant**1) # equivalent
]

app.band["drums"] = RythmicPlayer(100, drums_parts[0])
app.band["organ"] = TonalPlayer(100, organ_parts[0], MelodicInstrument.PercussiveOrgan)

# # test:
# app.band.play("drums", .4)
# app.band.play("organ", .4)

def change_drums_part(p: str):
    app.band["drums"].part = drums_parts[int(p)]

app.handlers["d"] = change_drums_part

app.start()
