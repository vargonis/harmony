from dataclasses import dataclass
from typing import Sequence
from numbers import Number
import asyncio
from threading import Thread

from .instruments import MelodicInstrument, PercussiveInstrument


@dataclass
class Pattern:
    n_beats: int
    rythm: list[tuple[int, int]] # beat start/duration on which clusters are to be played
    clusters: list[list[int]] # "chords" of the current mode (or percussions in the kit, if the player is rythmic) to be played, must have same length as `rythm`
    # dynamics: list[list[int]] # relative increase/decrease of volume on each note. Leave it out, for now

@dataclass
class Player:
    vol: int
    pattern: Pattern

    def play_in_loop(self, lapse: float, loop: asyncio.AbstractEventLoop):
        asyncio.run_coroutine_threadsafe(self.play(lapse), loop)

    # def play_in_thread(self, lapse: float):
    #     thread = Thread(target=asyncio.run, args=(self.play(lapse),))
    #     thread.start()

@dataclass
class TonalPlayer(Player):
    tone: float # base frequency
    mode: Sequence[Number] # harmonic scale
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


class Band(dict[str, Player]):

    def __init__(self):
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        def run():
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()
        self.thread = Thread(target=run)
        self.thread.start()

    def __setitem__(self, key: str, value):
        if not isinstance(value, Player):
            raise TypeError(f'Expected Player, got {type(value)}')
        return super().__setitem__(key, value)

    def play(self, lapse: float):
        for player in self.values():
            player.play_in_loop(lapse, self.loop)