import asyncio
import numpy as np

from microtonal.instruments import MelodicInstrument
from microtonal.harmony import GreekChord, GreekScale


asyncio.run(MelodicInstrument.PercussiveOrgan(300, 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 7/6, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * GreekChord.MAJOR, 100, 1))
asyncio.run(MelodicInstrument.YamahaGrandPiano(100 * GreekChord.MINOR, 100, 1))


def play_scale(base, scale, instrument, velocity, duration):
    async def coroutine():
        freq = base
        await instrument(freq, velocity, duration)
        for x in scale:
            freq *= x
            await instrument(freq, velocity, duration)
    asyncio.run(coroutine())

def play_arpeggio(base, chord, instrument, velocity, duration):
    async def coroutine():
        for x in chord:
            await instrument(base * x, velocity, duration)
    asyncio.run(coroutine())


play_arpeggio(100, GreekChord.MINOR, MelodicInstrument.Dulcimer, 100, .5)

play_scale(100, GreekScale.MAJOR, MelodicInstrument.YamahaGrandPiano, 100, .3)
play_scale(100, GreekScale.MINOR, MelodicInstrument.YamahaGrandPiano, 100, .1)


#%%
# A slightly more complex example. By the way, we need to come up with a good way of interacting with the system,
# one that turns it into an "instrument"... This is intended as a preliminary exploration.

async def test():
    base = 300
    delta = .3
    tasks = [
        MelodicInstrument.PercussiveOrgan(base, 90, 3),
        MelodicInstrument.YamahaGrandPiano(base, 127, .3, delay=delta),
    ]
    for x in GreekScale.MAJOR:
        base *= x
        delta += .3
        # s.schedule(MelodicInstrument.PercussiveOrgan(base, 127, .3), start + delta)
        tasks.append(MelodicInstrument.YamahaGrandPiano(base, 127, .3, delay=delta))
    await asyncio.gather(*tasks)

asyncio.run(test())
