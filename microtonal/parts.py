from __future__ import annotations
from dataclasses import dataclass, fields
from functools import total_ordering
from copy import deepcopy

from .instruments import PercussiveInstrument
from .harmony import Cluster


@total_ordering
@dataclass
class Event:
    start: float # beat number
    duration: float # in beats
    # intensity: float # Volume. Leave it out, for now

    def copy(self):
        return type(self)(*[deepcopy(self.__getattribute__(a.name)) for a in fields(self)])

    def __lt__(self, other: Event) -> bool:
        return (self.start, self.duration) < (other.start, other.duration)
    
    def __rmul__(self, other: list[T]) -> list[Event]:
        return [t * self for t in other]
    
    def __add__(self, other: Event) -> list[Event]:
        return [self, other]


@dataclass
class Note(Event):
    index: int
    mode: Cluster

@dataclass
class Hit(Event):
    instrument: PercussiveInstrument

@dataclass
class Chord(Event):
    cluster: Cluster

    def __pow__(self, other: int):
        return Chord(self.start, self.duration, self.cluster ** other)


# Convenience constructors:
def note(index: int, mode: Cluster):
    return Note(0, 1, index, mode)

def chord(cluster: Cluster):
    return Chord(0, 1, cluster)

def hit(instrument: PercussiveInstrument):
    return Hit(0, 1, instrument)


@dataclass
class Part:
    n_beats: int
    events: list[Event] | Event # second possibility just to facilitate construction: it would be converted to singleton on __post_init__

    def __post_init__(self):
        if isinstance(self.events, Event):
            self.events = [self.events]
        self.events.sort()

    def __add__(self, other: Part):
        if self.n_beats != other.n_beats:
            raise ValueError("Parts must have the same number of beats")
        events = deepcopy(self.events) + deepcopy(other.events)
        return Part(self.n_beats, events)

    def __mul__(self, other: Part):
        n_beats = self.n_beats + other.n_beats
        events = deepcopy(self.events) + [T(self.n_beats) * e for e in other.events]
        return Part(n_beats, events)
    
    def __rmul__(self, other: list[T]):
        return sum([s * self for s in other], start=Part(self.n_beats, []))

    def __pow__(self, n: int):
        part = self
        for _ in range(n - 1):
            part = self * part
        return part


@dataclass
class T:
    start: float
    duration: float = 1

    def __mul__(self, other: Event | Part | T | list[T]):
        if isinstance(other, Event):
            event = other.copy()
            event.start += self.start
            event.duration *= self.duration
            return event
        if isinstance(other, Part):
            return Part(other.n_beats, [self * e for e in other.events])
        if isinstance(other, T):
            return T(self.start + other.start, self.duration * other.duration)
        assert isinstance(other, list), f"Expected Event, Part, T or list, got {type(other)}"
        return [self * t for t in other]
    
    def __add__(self, other: T) -> list[T]:
        return [self, other]

    def __radd__(self, other: list[T]) -> list[T]:
        return other + [self]
