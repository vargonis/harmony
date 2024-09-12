from __future__ import annotations
from numbers import Number
from dataclasses import dataclass
from functools import total_ordering
from copy import deepcopy

from .harmony import Cluster


@total_ordering
@dataclass
class Note:
    value: float | int # frequency or index (for percussive instruments)
    start: float # beat number
    duration: float # in beats
    # dynamics: float # relative increase/decrease of volume within a pattern. Leave it out, for now

    def copy(self):
        return Note(self.value, self.start, self.duration)

    def __lt__(self, other: Note):
        return (self.start, self.duration, self.value) < (other.start, other.duration, other.value)

    def __add__(self, other: Note):
        return [self, other]
    
    def __radd__(self, other: list[Note]):
        return other + [self]
    
    def __rmul__(self, other: list[Shift]):
        return [s * self for s in other]


@dataclass
class Pattern:
    n_beats: int
    notes: list[Note] | list[Shift] # list[Shift] only to facilitate construction, it will me transformed into a list[Note] on __post_init__

    def __post_init__(self):
        def instantiate(x):
            note = x if isinstance(x, Note) else x * Note(1, 0, 1)
            note.start = note.start % self.n_beats
            return note
        if isinstance(self.notes, Note | Shift): # to facilitate initialization with a single note
            self.notes = [self.notes]
        self.notes = [instantiate(x) for x in self.notes]
        self.notes.sort()

    def __add__(self, other: Pattern):
        if self.n_beats != other.n_beats:
            raise ValueError("Patterns must have the same number of beats")
        notes = deepcopy(self.notes) + deepcopy(other.notes)
        notes.sort()
        return Pattern(self.n_beats, notes)

    def __mul__(self, other: Pattern):
        n_beats = self.n_beats + other.n_beats
        notes = deepcopy(self.notes) + [T(self.n_beats) * note for note in other.notes] # should already be sorted
        return Pattern(n_beats, notes)
    
    def __rmul__(self, other: list[Shift]):
        return sum([s * self for s in other], start=Pattern(self.n_beats, []))

    def __pow__(self, n: int):
        pattern = self
        for _ in range(n - 1):
            pattern = self * pattern
        return pattern


@dataclass
class Shift: # a shift in pitch and beat
    note: float | int
    beat: float
    sustain: float

    def __mul__(self, other: Note | Pattern | Number | Cluster | list | Shift):
        if isinstance(other, Note):
            return Note(other.value * self.note, other.start + self.beat, other.duration * self.sustain)
        if isinstance(other, Pattern):
            return Pattern(other.n_beats, [self * note for note in other.notes])
        if isinstance(other, Number):
            return self * Shift(other, 0, 1)
        if isinstance(other, Cluster):
            return [self * Note(x, 0, 1) for x in other.value]
        if isinstance(other, list):
            return [self * note for note in other]
        assert isinstance(other, Shift), f"Expected Note, Pattern, list or S, got {type(other)}"
        return Shift(self.note * other.note, self.beat + other.beat, self.sustain * other.sustain)
    
    def __add__(self, other: Shift):
        return [self, other]

    def __radd__(self, other: list[Shift]):
        return other + [self]


def S(note: float, beat: float = 0, sustain: float = 1):
    return Shift(note, beat, sustain)

def T(beat: float):
    return Shift(1, beat, 1)

def W(sustain: float):
    return Shift(1, 0, sustain)


def s(i: int):
    return Note(i, 0, 1)

# @dataclass
# class Shift_: # inplace version
#     beat: float
#     sustain: float
#     note: int
#     def __mul__(self, other: Note | Pattern | Shift_):
#         if isinstance(other, Note):
#             other.start += self.beat; other.duration *= self.sustain; other.index += self.note
#             return other
#         if isinstance(other, Pattern):
#             for note in other.notes:
#                 self * note
#             other.__post_init__()
#             return other
#         if isinstance(other, list):
#             for note in other:
#                 self * note 
#             return other
#         assert isinstance(other, Shift_), f"Expected Note, Pattern, list or S_, got {type(other)}"
#         return Shift_(self.beat + other.beat, self.sustain * other.sustain, self.note + other.note)

# def S_(note: int):
#     return Shift_(0, 1, note)

# def T_(beat: float):
#     return Shift_(beat, 1, 0)

# def W_(sustain: float):
#     return Shift_(0, sustain, 0)
