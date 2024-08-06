from enum import Enum
import numpy as np

class IterableEnum(Enum):
    def __iter__(self):
        return iter(self.value) 
    def __len__(self):
        return len(self.value)

class GreekChord(IterableEnum):
    MAJOR = [1, 5/4, 3/2]
    MINOR = [1, 6/5, 3/2]
    def __rmul__(self, x):
        return np.array(self.value) * x

class GreekScale(IterableEnum):
    MAJOR = [9/8, 10/9, 16/15, 9/8, 10/9, 9/8, 16/15]
    MINOR = [9/8, 16/15, 10/9, 9/8, 16/15, 10/9, 9/8]

