from random import randint

from microtonal.instruments import MelodicInstrument
from microtonal.harmony import ChordType
from microtonal.parts import note, chord, Part, T
from microtonal.players import Band, TonalPlayer
from microtonal.repl import App

app = App(
    band = Band(),
    tempo = .4,
)

mode = 300 * (
    ChordType.II + # 4/3 * Chord.II + # 16/9 * Chord.II + 
    3/4 * ChordType.II # + 9/16 * Chord.II
)

def rand_part():
    return Part(8, [T(i) * note(randint(-6, 6), mode) for i in range(8)])

parts = [rand_part() for _ in range(3)]

chord_1 = chord(300 * ChordType.II)
chord_2 = chord(3/4 * 300 * ChordType.II)

app.band["bed"] = TonalPlayer(80, Part(8, T(0,6) * chord_1 + T(6,2) * chord_2), MelodicInstrument.AhhChoir)
app.band["melody"] = TonalPlayer(110, parts[0], MelodicInstrument.Clarinet)

# # test:
# app.band.play("bed", .4)
# app.band.play("melody", .4)

def change_melody(p: str):
    app.band["melody"].part = parts[int(p)]

app.handlers["m"] = change_melody

app.start()
