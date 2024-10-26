from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.harmony import Major, minor, T
from microtonal.events import chord, hit, at
from microtonal.players import Band, TonalPlayer, RythmicPlayer, Part
from microtonal.repl import App

app = App(
    band = Band(),
    tempo = .4,
)

d = hit(PercussiveInstrument.AcousticBassDrum)

s = hit(PercussiveInstrument.AcousticSnare)
r = hit(PercussiveInstrument.RideCymbal1)
snare = Part(2, at(1) * s)
drum_1 = Part(8, (at(0) + at(1.5) + at(6.5)) * d)
drum_2 = Part(8, (at(0) + at(1.5) + at(4.5) + at(6) + at(6.5)) * d)
ride = Part(1, r)
drums_parts = [
    drum_1 + snare**4,
    drum_2 + snare**4 + ride**8,
]
# d.play()

base = 300
tonic = chord(Major(3, base))
subdominant = chord(Major(3, 3/4 * base))
# tonic.play(MelodicInstrument.PercussiveOrgan)
# (subdominant**T(2)).play(MelodicInstrument.PercussiveOrgan)

organ_parts = [
    Part(6, at(0,6) * tonic) * Part(2, at(0,2) * subdominant**T(2))
    # Part(8, at(0,6) * tonic + at(6,2) * subdominant**T(2)) # equivalent
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
