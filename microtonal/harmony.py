from dataclasses import dataclass
from numbers import Number
import numpy as np


def normalize(x):
    "Returns 2^n*x, where n is the integer such that 1 <= 2^n*x < 2."
    return np.pow(2, np.mod(np.log2(x), 1))

@dataclass
class T:
    "Chord inversion operator."
    n: int
    "Inversion number."

@dataclass
class Cluster:
    values: np.ndarray

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key: int):
        "When key is out of the range of the cluster, we cycle around but rescaling the cluster values by a factor of 2."
        n, k = divmod(key, len(self.values))
        return self.values[k] * 2**n

    def __rmul__(self, x: Number):
        "Shifts the cluster values multiplicatively."
        if not isinstance(x, Number):
            raise TypeError(f'Expected a number, got {type(x)}')
        return Cluster(x * self.values)

    # def extend(self, other: 'Cluster'):
    #     """
    #     Returns a cluster that is the concatenation of `self` with `other`, shifted in a way that its first tone coincides with the last tone of `self`.
    #     Note that this, though, assumes that `other`s first tone is 1. Note also that extending a I-type chord by a II-type chord duplicates the tonic,
    #     so we might need a better interface.
    #     """
    #     return Cluster(np.concat([self, (self[len(self) - 1] * other)[1:]]))
    
    def __pow__(self, other: T):
        """
        Inverts the cluster, the number of specified times.
        """
        if other.n == 0:
            return self
        if other.n > 0:
            return Cluster(np.concatenate([self.values[other.n:], 2 * self.values[:other.n]]))
        return Cluster(np.concatenate([0.5 * self.values[len(self.values) + other.n:], self.values[:len(self.values) + other.n]]))

    def __add__(self, other: 'Cluster'):
        return Cluster(np.sort(np.unique(np.concatenate([
            normalize(self), normalize(other)
        ]))))

def Major(n, fundamental=1) -> Cluster:
    return fundamental * Cluster(np.array([i for i in range(n, 2*n)]) / n)

def minor(n, fundamental=1) -> Cluster:
    return fundamental * Cluster(2*n / np.array([i for i in range(2*n, n, -1)]))


"""
Notes:

    Major(3): this is a transposed major chord!
    Major(4): this is the standard major chord, plus somehting like a seventh (I_II above)
    Major(6): this is the pentatonic scale I wanted to explore, plus the 11/6 at the end
    Major(8): this is close to the major scale
    Major(12): is this something like a chromatic scale?

    Cluster(7 / np.array([7, 6, 5, 4])) is something like a `minor(3.5)`. It is a sub-cluster of `minor(7)`
    
"""
