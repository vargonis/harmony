from abc import ABC, abstractmethod
from dataclasses import dataclass
import asyncio
from threading import Thread

from .synth import Synth
from .parts import Part, Note, Chord, Hit
from .instruments import MelodicInstrument

synth = Synth()


@dataclass
class Player(ABC):
    vol: int # velocity, in midi messages (will be rescaled by the intensity of the played events)
    part: Part

    @abstractmethod
    async def play(self, tempo: float):
        ...

    def play_in_loop(self, tempo: float, loop: asyncio.AbstractEventLoop):
        asyncio.run_coroutine_threadsafe(self.play(tempo), loop)

    # def play_in_thread(self, tempo: float):
    #     thread = Thread(target=asyncio.run, args=(self.play(tempo),))
    #     thread.start()

@dataclass
class TonalPlayer(Player):
    instrument: MelodicInstrument

    def __post_init__(self):
        assert all(isinstance(e, Note) or isinstance(e, Chord) for e in self.part.events)

    async def play(self, tempo: float):
        tasks = []
        for e in self.part.events:
            if isinstance(e, Note):
                task = synth.play(
                    self.instrument,
                    e.mode[e.index],
                    round(self.vol * e.intensity),
                    e.duration * tempo,
                    e.start * tempo,
                )
            else:
                assert isinstance(e, Chord)
                task = synth.play_chord(
                    self.instrument,
                    e.cluster.values,
                    round(self.vol * e.intensity),
                    e.duration * tempo,
                    e.start * tempo,
                )
            tasks.append(task)
        await asyncio.gather(*tasks)

@dataclass
class RythmicPlayer(Player):

    def __post_init__(self):
        assert all(isinstance(e, Hit) for e in self.part.events)

    async def play(self, tempo: float):
        tasks = []
        for hit in self.part.events:
            tasks.append(
                hit.instrument(round(self.vol * hit.intensity), hit.start * tempo)
            )
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

    # NOTE: this method does not play all players in the band at the same time, because that would make it hard to have parts with different lengths.
    def play(self, player: str, tempo: float):
        self[player].play_in_loop(tempo, self.loop)