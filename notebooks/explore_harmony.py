import asyncio
import numpy as np

from microtonal.instruments import MelodicInstrument
from microtonal.harmony import GreekChord


async def play_arpeggio(program, base, chord, velocity, duration):
    for x in chord:
        await program(base * x, velocity, duration)

#%%
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 7/6]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 7/6, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 8/7, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(400 * np.array([1, 8/7, 4/3]), 100, 1))

for _ in range(3):
    asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 7/6, 4/3]), 100, 1))
    asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 3/2, 7/4]), 100, 1))

for _ in range(3):
    asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1/2, 7/6, 4/3]), 100, 1))
    asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1/2, 7/8, 3/2]), 100, 1))


asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 7/6, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * 4/3 * np.array([1, 7/6, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([3/2, 7/4, 2]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 7/6, 4/3]), 100, 1))

asyncio.run(MelodicInstrument.PercussiveOrgan(300 * np.array([1, 7/6, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * 5/4 * np.array([1, 7/6, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * 4/3 * np.array([1, 7/6, 4/3]), 100, 1))
asyncio.run(MelodicInstrument.PercussiveOrgan(300 * GreekChord.MAJOR, 100, 1))


#%%
base = 200
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 4/3, 3/2, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 7/6, 4/3, 3/2, 7/4, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.YamahaGrandPiano, base, [1, 7/6, 4/3, 3/2, 7/4, 2], 127, .7))

asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 9/8, 7/6, 6/5, 5/4, 4/3, 3/2, 8/5, 7/4, 16/9, 15/8, 2], 127, .5))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 9/8, 5/4, 4/3, 3/2, 7/4, 15/8, 2], 127, .5))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2], 127, .5))

asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 9/8, 7/6, 5/4, 4/3, 3/2, 5/3, 7/4, 15/8, 2], 127, .5))

asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 7/6, 9/7, 4/3, 3/2, 7/4, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 7/6, 9/7, 3/2, 12/7, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 8/7, 9/7, 3/2, 12/7, 2], 127, .7))

asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 8/9, 4/5, 3/2, 7/4, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 8/9, 4/5, 2/3, 4/7, 1/2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 9/8, 5/4, 3/2, 7/4, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 10/9, 5/4, 3/2, 7/4, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 10/9, 5/4, 3/2, 12/7, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, base, [1, 10/9, 5/4, 3/2, 17/7, 2], 127, .7))

asyncio.run(play_arpeggio(MelodicInstrument.BowedGlass, base, [1, 10/9, 5/4, 3/2, 17/7, 2], 127, .7))

asyncio.run(play_arpeggio(MelodicInstrument.BowedGlass, base, [1, 8/7, 9/7, 10/7, 11/7, 12/7, 13/7, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Clarinet, base, [1, 8/7, 9/7, 10/7, 11/7, 12/7, 13/7, 2, 13/7, 12/7, 11/7, 10/7, 9/7, 8/7, 1], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Clarinet , base, [1, 7/6, 8/6, 9/6, 10/6, 11/6, 2], 127, .7))

asyncio.run(play_arpeggio(MelodicInstrument.Clarinet , base, [1, 7/6, 8/6, 9/6, 10/6, 11/6, 2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Clarinet , base, [1, 7/6, 8/6, 9/6, 10/6, 11/6, 2, 11/6, 10/6, 9/6, 8/6, 7/6, 1], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Clarinet , 2 * base, [1/2, 6/11, 6/10, 6/9, 6/8, 6/7, 1, 6/7, 6/8, 6/9, 6/10, 6/11, 1/2], 127, .7))
asyncio.run(play_arpeggio(MelodicInstrument.Clarinet , 2 * base, [6/12, 6/11, 6/10, 6/9, 6/8, 6/9, 6/10, 6/11, 6/12], 127, .7))

asyncio.run(play_arpeggio(MelodicInstrument.Clarinet , base, [1, 7/6, 8/6, 9/6, 8/6, 7/6, 1], 127, .7))
asyncio.run(MelodicInstrument.Clarinet(base * np.array([1]), 100, 2))
asyncio.run(MelodicInstrument.Clarinet(base * np.array([1, 7/6]), 100, 2))
asyncio.run(MelodicInstrument.Clarinet(base * np.array([1, 7/6, 8/6]), 100, 2))
asyncio.run(MelodicInstrument.Clarinet(base * np.array([1, 7/6, 8/6, 9/6]), 100, 2))

#%%
asyncio.run(play_arpeggio(MelodicInstrument.Fiddle, 300, [1, 7/6, 4/3], 127, .5))
asyncio.run(play_arpeggio(MelodicInstrument.Clarinet, 220, [1, 6/5, 4/3], 127, .5))
