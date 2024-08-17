import time
import blinker

from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.harmony import GreekMode
from microtonal.patterns import Note, Pattern, S, T, W
from microtonal.players import Band, TonalPlayer, RythmicPlayer

band = Band()

kit = [PercussiveInstrument.AcousticBassDrum, PercussiveInstrument.AcousticSnare, PercussiveInstrument.RideCymbal1]
b = Note(0, 1, 0)
s = Note(0, 1, 1)
r = Note(0, 1, 2)
pattern = Pattern(2, b + T(1) * s)**2 + Pattern(1, r)**4
band["drummer"] = RythmicPlayer(100, pattern, kit)
# Test:
band["drummer"].play_in_loop(1, band.loop)

n = Note(0, 1, 0)
t = n + S(2) * n + S(4) * n
s = n + S(3) * n + S(5) * n
pattern = Pattern(3, W(3) * t) * Pattern(1, s)
band["organ"] = TonalPlayer(100, pattern, 200 * GreekMode.MAJOR, MelodicInstrument.PercussiveOrgan)
# Test:
band["organ"].play_in_loop(1, band.loop)


# Ready to go:
measure = blinker.signal("measure")

measure.connect(band.play)
# measure.disconnect(band.play)

for _ in range(3):
    measure.send(1.2)
    time.sleep(1.2)
