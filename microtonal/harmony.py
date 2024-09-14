from dataclasses import dataclass
from numbers import Number
import numpy as np
from types import ModuleType


def normalize(x):
    return np.pow(2, np.mod(np.log2(x), 1))

@dataclass
class Cluster:
    values: np.ndarray

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key: int):
        n, k = divmod(key, len(self.value))
        return self.values[k] * 2**n

    def __rmul__(self, x):
        if not isinstance(x, Number):
            raise TypeError(f'Expected a number, got {type(x)}')
        return Cluster(x * self.values)

    def extend(self, other: 'Cluster'):
        return Cluster(np.concat([self, (self[len(self) - 1] * other)[1:]]))
    
    def __pow__(self, other: int):
        if other == 0:
            return self
        if other > 0:
            return Cluster(np.concatenate([self.values[other:], 2 * self.values[:other]]))
        return Cluster(np.concatenate([0.5 * self.values[len(self.values) + other:], self.values[:len(self.values) + other]]))

    def __add__(self, other: 'Cluster'):
        return Cluster(np.sort(np.unique(np.concatenate([
            normalize(self), normalize(other)
        ]))))


class ChordType(ModuleType):
    I = Cluster(np.array([1, 5/4, 3/2]))
    Im = Cluster(np.array([1, 6/5, 3/2]))
    II = Cluster(np.array([1, 7/6, 4/3]))
    IIm = Cluster(np.array([1, 8/7, 4/3]))

class GreekChord(ModuleType):
    MAJOR = ChordType.I
    MINOR = ChordType.Im

class GreekMode(ModuleType):
    MAJOR = Cluster(np.array([1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8])) # == Chord.I + 3/2*Chord.I + 4/3*Chord.I
    MINOR = Cluster(np.array([1, 9/8, 6/5, 4/3, 3/2, 8/5, 16/9]))

# class GreekScale(IterableEnum):
#     MAJOR = [9/8, 10/9, 16/15, 9/8, 10/9, 9/8, 16/15]
#     MINOR = [9/8, 16/15, 10/9, 9/8, 16/15, 10/9, 9/8]

