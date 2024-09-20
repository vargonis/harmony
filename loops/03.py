from microtonal.instruments import MelodicInstrument
from microtonal.harmony import ChordType
from microtonal.parts import Part, Chord
from microtonal.players import Band, TonalPlayer
from microtonal.repl import App


app = App(
    band = Band(),
    tempo = .4,
)

c = 8/9
b1 = Part(4, Chord(0, 4, 1, 250 * ChordType.Im))
b2 = Part(4, Chord(0, 4, 1, 250 * ChordType.II))
b3 = Part(4, Chord(0, 4, 1, 250 * c * ChordType.I))
b4 = Part(4, Chord(0, 4, 1, 250 * c * ChordType.IIm))
b5 = Part(4, Chord(0, 4, 1, 250 * c**2 * ChordType.Im))
b6 = Part(4, Chord(0, 4, 1, 250 * c**2 * ChordType.II))
b7 = Part(4, Chord(0, 4, 1, 250 * c**3 * ChordType.I))
b8 = Part(4, Chord(0, 4, 1, 250 * 3/4 * ChordType.I_II))

app.band["bed"] = TonalPlayer(80, b1 * b2 * b3 * b4 * b5 * b6 * b7 * b8, MelodicInstrument.AhhChoir)

app.start()
