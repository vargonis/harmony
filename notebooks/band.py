import time
import blinker

from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.greek import GreekMode
from microtonal.players import Band, TonalPlayer, RythmicPlayer, Pattern

band = Band()

pattern = Pattern(4, [(0, 1), (1, 1), (2, 1), (3, 1)], [[0, 2], [1, 2], [0, 2], [1, 2]])
band["drummer"] = RythmicPlayer(
    100, pattern,
    [PercussiveInstrument.AcousticBassDrum, PercussiveInstrument.AcousticSnare, PercussiveInstrument.RideCymbal1],
)
# Test:
band["drummer"].play_in_loop(1, band.loop)

pattern = Pattern(4, [(0, 3), (3, 1)], [[0, 2, 4], [0, 3, 5]])
band["organ"] = TonalPlayer(100, pattern, 200, GreekMode.MAJOR, MelodicInstrument.PercussiveOrgan)
# Test:
band["organ"].play_in_loop(1, band.loop)


# Ready to go:
measure = blinker.signal("measure")

measure.connect(band.play)
# measure.disconnect(band.play)

for _ in range(3):
    measure.send(1.2)
    time.sleep(1.2)
