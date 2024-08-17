from __future__ import annotations
from dataclasses import dataclass
from functools import total_ordering
from copy import deepcopy


@total_ordering
@dataclass
class Note:
    start: float # beat number
    duration: float # in beats
    index: int # relative to the current mode
    # dynamics: float # relative increase/decrease of volume within a pattern. Leave it out, for now

    def copy(self):
        return Note(self.start, self.duration, self.index)

    def __lt__(self, other: Note):
        return (self.start, self.duration, self.index) < (other.start, other.duration, other.index)

    def __add__(self, other: Note):
        return [self, other]
    
    def __radd__(self, other: list[Note]):
        return other + [self]
    
    def __rmul__(self, other: int):
        return Note(self.start, self.duration * other, self.index)


@dataclass
class Pattern:
    n_beats: int
    notes: list[Note]
    
    def __post_init__(self):
        if isinstance(self.notes, Note): # to facilitate initialization with a single note
            self.notes = [self.notes]
        for note in self.notes:
            note.start = note.start % self.n_beats
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

    def __pow__(self, n: int):
        pattern = self
        for _ in range(n - 1):
            pattern = self * pattern
        return pattern


@dataclass
class Shift: # a shift in pitch and beat
    beat: float
    sustain: float
    note: int
    def __mul__(self, other: Note | Pattern | Shift):
        if isinstance(other, Note):
            return Note(other.start + self.beat, other.duration * self.sustain, other.index + self.note)
        if isinstance(other, Pattern):
            return Pattern(other.n_beats, [self * note for note in other.notes])
        if isinstance(other, list):
            return [self * note for note in other]
        assert isinstance(other, Shift), f"Expected Note, Pattern, list or S, got {type(other)}"
        return Shift(self.beat + other.beat, self.sustain * other.sustain, self.note + other.note)

@dataclass
class Shift_: # inplace version
    beat: float
    sustain: float
    note: int
    def __mul__(self, other: Note | Pattern | Shift_):
        if isinstance(other, Note):
            other.start += self.beat; other.duration *= self.sustain; other.index += self.note
            return other
        if isinstance(other, Pattern):
            for note in other.notes:
                self * note
            other.__post_init__()
            return other
        if isinstance(other, list):
            for note in other:
                self * note 
            return other
        assert isinstance(other, Shift_), f"Expected Note, Pattern, list or S_, got {type(other)}"
        return Shift_(self.beat + other.beat, self.sustain * other.sustain, self.note + other.note)

def S(note: int):
    return Shift(0, 1, note)

def S_(note: int):
    return Shift_(0, 1, note)

def T(beat: float):
    return Shift(beat, 1, 0)

def T_(beat: float):
    return Shift_(beat, 1, 0)

def W(sustain: float):
    return Shift(0, sustain, 0)

def W_(sustain: float):
    return Shift_(0, sustain, 0)
