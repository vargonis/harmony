from dataclasses import dataclass
from fractions import Fraction
import asyncio
from threading import Thread
import time
import blinker

from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.greek import GreekChord, GreekScale


@dataclass
class Pattern:
    n_beats: int
    rythm: list[tuple[int, int]] # beat start/duration on which clusters are to be played
    clusters: list[list[int]] # "chords" of the current mode (or percussions in the kit, if the player is rythmic) to be played, must have same length as `rythm`
    # dynamics: list[list[int]] # relative increase/decrease of volume on each note. Leave it out, for now

@dataclass
class Player:
    loop: asyncio.AbstractEventLoop
    vol: int
    pattern: Pattern

    def play_in_loop(self, lapse: float):
        asyncio.run_coroutine_threadsafe(self.play(lapse), self.loop)

    def play_in_thread(self, lapse: float):
        thread = Thread(target=asyncio.run, args=(self.play(lapse),))
        thread.start()

@dataclass
class TonalPlayer(Player):
    tone: float # base frequency
    mode: list[Fraction] # harmonic scale
    instrument: MelodicInstrument # midi terminology: the instrument's program number

    async def play(self, lapse: float):
        tasks = []
        for cluster, (start, duration) in zip(self.pattern.clusters, self.pattern.rythm):
            for i in cluster:
                tasks.append(self.instrument(
                    self.tone * self.mode[i],
                    self.vol,
                    duration * lapse / self.pattern.n_beats,
                    start * lapse / self.pattern.n_beats),
                )
        await asyncio.gather(*tasks)

@dataclass
class RythmicPlayer(Player):
    kit: list[PercussiveInstrument]

    async def play(self, lapse: float):
        tasks = []
        for cluster, (beat, _) in zip(self.pattern.clusters, self.pattern.rythm):
            for i in cluster:
                tasks.append(self.kit[i](
                    self.vol,
                    beat * lapse / self.pattern.n_beats,
                ))
        await asyncio.gather(*tasks)


loop = asyncio.new_event_loop()

def run(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

t = Thread(target=run, args=(loop,))
t.start()


pattern = Pattern(4, [(0, 1), (1, 1), (2, 1), (3, 1)], [[0, 2], [1, 2], [0, 2], [1, 2]])
drummer = RythmicPlayer(
    loop, 100, pattern,
    [PercussiveInstrument.AcousticBassDrum, PercussiveInstrument.AcousticSnare, PercussiveInstrument.RideCymbal1],
)
# Test:
drummer.play_in_thread(1)
drummer.play_in_loop(1)

pattern = Pattern(4, [(0, 3), (3, 1)], [[0, 2, 4], [0, 3, 5]])
organ = TonalPlayer(loop, 100, pattern, 200, [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8], MelodicInstrument.PercussiveOrgan)
# Test:
organ.play_in_loop(1)


# Ready to go:
measure = blinker.signal("measure")

# measure.connect(drummer.play_in_thread)
# measure.connect(organ.play_in_thread)
# # measure.disconnect(drummer.play_in_thread)
# # measure.disconnect(organ.play_in_thread)

measure.connect(drummer.play_in_loop)
measure.connect(organ.play_in_loop)

for _ in range(3):
    measure.send(1.2)
    time.sleep(1.2)


#%%
import curses
import os

def main(win):
    win.nodelay(True)
    win.clear()                
    win.addstr("Detected key:")
    key = ""
    while 1:          
        try:                 
            key = win.getkey()         
            win.clear()                
            win.addstr("Detected key:")
            win.addstr(str(key)) 
            measure.send(1)
            if key == os.linesep:
                break           
        except Exception as e:
            # No input   
            pass         

curses.wrapper(main)