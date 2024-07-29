from enum import Enum
import mido

from .output import output

class Percussion(Enum):
    AcousticBassDrum = 35
    ElectricBassDrum = 36
    SideStick = 37
    AcousticSnare = 38
    HandClap = 39
    ElectricSnare = 40
    LowFloorTom = 41
    ClosedHihat = 42
    HighFloorTom = 43
    PedalHihat = 44
    LowTom = 45
    OpenHihat = 46
    LowMidTom = 47
    HighMidTom = 48
    CrashCymbal1 = 49
    HighTom = 50
    RideCymbal1 = 51
    ChineseCymbal = 52
    RideBell = 53
    Tambourine = 54
    SplashCymbal = 55
    Cowbell = 56
    CrashCymbal2 = 57
    Vibraslap = 58
    RideCymbal2 = 59
    HighBongo = 60
    LowBongo = 61
    MuteHighConga = 62
    OpenHighConga = 63
    LowConga = 64
    HighTimbale = 65
    LowTimbale = 66
    HighAgogo = 67
    LowAgogo = 68
    Cabasa = 69
    Maracas = 70
    ShortWhistle = 71
    LongWhistle = 72
    ShortGuiro = 73
    LongGuiro = 74
    Claves = 75
    HighWoodblock = 76
    LowWoodblock = 77
    MuteCuica = 78
    OpenCuica = 79
    MuteTriangle = 80
    OpenTriangle = 81

    def __call__(self, velocity):
        output.send(mido.Message('note_on', channel=9, note=self.value, velocity=velocity))
