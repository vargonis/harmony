from typing import Sequence
from numbers import Number
from dataclasses import dataclass
import asyncio
from threading import Thread

from .patterns import Pattern
from .instruments import MelodicInstrument, PercussiveInstrument


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
    mode: Sequence[Number] # harmonic scale
    instrument: MelodicInstrument # midi terminology: the instrument's program number

    async def play(self, lapse: float):
        tasks = []
        for note in self.pattern.notes:
            tasks.append(self.instrument(
                self.mode[note.index],
                self.vol,
                note.duration * lapse / self.pattern.n_beats,
                note.start * lapse / self.pattern.n_beats),
            )
        await asyncio.gather(*tasks)

@dataclass
class RythmicPlayer(Player):
    kit: list[PercussiveInstrument]

    async def play(self, lapse: float):
        tasks = []
        for note in self.pattern.notes:
            tasks.append(self.kit[note.index](
                self.vol,
                note.start * lapse / self.pattern.n_beats,
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