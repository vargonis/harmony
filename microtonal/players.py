from abc import ABC, abstractmethod
from dataclasses import dataclass
from copy import deepcopy
import asyncio
from threading import Thread

from . import synth
from .events import Event, Note, Chord, Hit, at
from .instruments import MelodicInstrument


@dataclass
class Part:
    n_beats: int
    events: list[Event] | Event # second possibility just to facilitate construction: it would be converted to singleton on __post_init__

    def __post_init__(self):
        if isinstance(self.events, Event):
            self.events = [self.events]
        self.events.sort()

    def __add__(self, other: 'Part'):
        if self.n_beats != other.n_beats:
            raise ValueError("Parts must have the same number of beats")
        events = deepcopy(self.events) + deepcopy(other.events)
        return Part(self.n_beats, events)

    def __mul__(self, other: 'Part'):
        n_beats = self.n_beats + other.n_beats
        events = deepcopy(self.events) + [at(self.n_beats) * e for e in other.events]
        return Part(n_beats, events)
    
    def __rmul__(self, other: list[at]):
        return sum([s * self for s in other], start=Part(self.n_beats, []))

    def __pow__(self, n: int):
        part = self
        for _ in range(n - 1):
            part = self * part
        return part


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
                task = synth.play_note(
                    self.instrument.value,
                    e.frequency,
                    round(self.vol * e.intensity),
                    e.duration * tempo,
                    e.start * tempo,
                )
            else:
                assert isinstance(e, Chord)
                task = synth.play_chord(
                    self.instrument.value,
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
            tasks.append(synth.play_hit(hit.instrument.value, round(self.vol * hit.intensity), hit.start * tempo))
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