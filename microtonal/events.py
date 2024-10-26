from __future__ import annotations
from dataclasses import dataclass, fields
from functools import total_ordering
from copy import deepcopy
from numbers import Number
import asyncio

from . import synth
from .harmony import Cluster, T
from .instruments import MelodicInstrument, PercussiveInstrument


@total_ordering
@dataclass
class Event:
    start: float # beat number
    duration: float # in beats
    intensity: float # volume (normalized)

    def copy(self):
        return type(self)(*[deepcopy(self.__getattribute__(a.name)) for a in fields(self)])

    def __lt__(self, other: Event) -> bool:
        return (self.start, self.duration, self.intensity) < (other.start, other.duration, other.intensity)
    
    def __rmul__(self, other: list[at]) -> list[Event]:
        return [t * self for t in other]
    
    def __add__(self, other: Event) -> list[Event]:
        return [self, other]


@dataclass
class Note(Event):
    frequency: Number

    def play(self, instrument: MelodicInstrument):
        asyncio.run(synth.play_note(instrument.value, self.frequency, round(127 * self.intensity), self.duration))


@dataclass
class Hit(Event):
    instrument: PercussiveInstrument

    def play(self):
        asyncio.run(synth.play_hit(self.instrument.value, round(127 * self.intensity)))


@dataclass
class Chord(Event):
    cluster: Cluster

    def play(self, instrument: MelodicInstrument):
        asyncio.run(synth.play_chord(instrument.value, self.cluster, round(127 * self.intensity), self.duration))

    def play_arpeggio(self, instrument: MelodicInstrument, note_duration=.3):
        for x in self.cluster:
            asyncio.run(synth.play_note(instrument.value, x, round(127 * self.intensity), note_duration))
        asyncio.run(synth.play_note(instrument.value, self.cluster[len(self.cluster)], round(127 * self.intensity), note_duration))

    def __pow__(self, other: T):
        return Chord(self.start, self.duration, self.intensity, self.cluster ** other)


# Convenience constructors:
def note(index: int, mode: Cluster, vol=1):
    return Note(0, 1, vol, mode[index])

def chord(cluster: Cluster, vol=1): # TODO: add support for chords with non-homogeneous note intensities
    return Chord(0, 1, vol, cluster)

def hit(instrument: PercussiveInstrument, vol=1):
    return Hit(0, 1, vol, instrument)


@dataclass
class at:
    start: float
    duration: float = 1
    intensity: float = 1

    # def __mul__(self, other: Event | Part | at | list[at]):
    def __mul__(self, other: Event | at | list[at]):
        if isinstance(other, Event):
            event = other.copy()
            event.start += self.start
            event.duration *= self.duration
            event.intensity *= self.intensity
            return event
        # if isinstance(other, Part):
        #     return Part(other.n_beats, [self * e for e in other.events])
        if isinstance(other, at):
            return T(self.start + other.start, self.duration * other.duration, self.intensity * other.intensity)
        assert isinstance(other, list), f"Expected Event, Part, T or list, got {type(other)}"
        return [self * t for t in other]
    
    def __add__(self, other: at) -> list[at]:
        return [self, other]

    def __radd__(self, other: list[at]) -> list[at]:
        return other + [self]
