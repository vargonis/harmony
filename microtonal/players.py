from dataclasses import dataclass
import asyncio
from threading import Thread

from .patterns import Pattern
from .instruments import MelodicInstrument, PercussiveInstrument


@dataclass
class Player:
    vol: int
    pattern: Pattern # TODO: vol should be part of pattern

    def play_in_loop(self, tempo: float, loop: asyncio.AbstractEventLoop):
        asyncio.run_coroutine_threadsafe(self.play(tempo), loop)

    # def play_in_thread(self, tempo: float):
    #     thread = Thread(target=asyncio.run, args=(self.play(tempo),))
    #     thread.start()

@dataclass
class TonalPlayer(Player):
    # mode: Sequence[Number] # harmonic scale
    instrument: MelodicInstrument # midi terminology: the instrument's program number

    async def play(self, tempo: float):
        tasks = []
        for note in self.pattern.notes:
            tasks.append(self.instrument(
                note.value,
                self.vol,
                note.duration * tempo,
                note.start * tempo),
            )
        await asyncio.gather(*tasks)
        self.callback()

@dataclass
class RythmicPlayer(Player):
    kit: list[PercussiveInstrument]

    async def play(self, tempo: float):
        tasks = []
        for note in self.pattern.notes:
            tasks.append(self.kit[note.value](
                self.vol,
                note.start * tempo,
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

    # NOTE: this method does not play all players in the band at the same time, because that would make it hard to have patterns with different lengths.
    def play(self, player: str, tempo: float):
        self[player].play_in_loop(tempo, self.loop)