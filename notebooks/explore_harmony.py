from microtonal.instruments import MelodicInstrument
from microtonal.harmony import Major, minor
from microtonal.events import chord


chord(Major(3, 300)).play(MelodicInstrument.Fiddle)
chord(minor(3, 300)).play(MelodicInstrument.Fiddle)

chord(Major(4, 300)).play(MelodicInstrument.Fiddle)
chord(minor(4, 300)).play(MelodicInstrument.Fiddle)

chord(Major(5, 300)).play(MelodicInstrument.Fiddle)
chord(minor(5, 300)).play(MelodicInstrument.Fiddle)

chord(Major(6, 300)).play(MelodicInstrument.Fiddle)
chord(minor(6, 300)).play(MelodicInstrument.Fiddle)


chord(Major(8, 300)).play_arpeggio(MelodicInstrument.Fiddle)
chord(minor(8, 300)).play_arpeggio(MelodicInstrument.Fiddle)

chord(Major(12, 300)).play_arpeggio(MelodicInstrument.Fiddle)
chord(minor(12, 300)).play_arpeggio(MelodicInstrument.Fiddle)


for _ in range(5):
    chord(Major(3, 300)).play_arpeggio(MelodicInstrument.Fiddle)
    chord(minor(3, 300)).play_arpeggio(MelodicInstrument.Fiddle)


chord(Major(5, 300)).play_arpeggio(MelodicInstrument.Fiddle)
chord(minor(5, 300)).play_arpeggio(MelodicInstrument.Fiddle)

chord(Major(6, 300)).play_arpeggio(MelodicInstrument.Fiddle)
chord(minor(6, 300)).play_arpeggio(MelodicInstrument.Fiddle)

chord(Major(7, 300)).play_arpeggio(MelodicInstrument.Fiddle)
chord(minor(7, 300)).play_arpeggio(MelodicInstrument.Fiddle)

chord(Major(9, 300)).play_arpeggio(MelodicInstrument.Fiddle)
chord(minor(9, 300)).play_arpeggio(MelodicInstrument.Fiddle)
