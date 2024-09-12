from enum import Enum
from numbers import Number
import asyncio
import mido

from . import output
from .synth import Synth

synth = Synth()


class MelodicInstrument(Enum):
    YamahaGrandPiano = 0
    BrightYamahaGrand = 1
    ElectricPiano = 2
    HonkyTonk = 3
    RhodesEP = 4
    LegendEP2 = 5
    Harpsichord = 6
    Clavinet = 7
    Celesta = 8
    Glockenspiel = 9
    MusicBox = 10
    Vibraphone = 11
    Marimba = 12
    Xylophone = 13
    TubularBells = 14
    Dulcimer = 15
    DrawbarOrgan = 16
    PercussiveOrgan = 17
    RockOrgan = 18
    ChurchOrgan = 19
    ReedOrgan = 20
    Accordion = 21
    Harmonica = 22
    Bandoneon = 23
    NylonStringGuitar = 24
    SteelStringGuitar = 25
    JazzGuitar = 26
    CleanGuitar = 27
    PalmMutedGuitar = 28
    OverdriveGuitar = 29
    DistortionGuitar = 30
    GuitarHarmonics = 31
    AcousticBass = 32
    FingeredBass = 33
    PickedBass = 34
    FretlessBass = 35
    SlapBass = 36
    PopBass = 37
    SynthBass1 = 38
    SynthBass2 = 39
    Violin = 40
    Viola = 41
    Cello = 42
    Contrabass = 43
    Tremolo = 44
    PizzicatoSection = 45
    Harp = 46
    Timpani = 47
    Strings = 48
    SlowStrings = 49
    SynthStrings1 = 50
    SynthStrings2 = 51
    AhhChoir = 52
    OhhVoices = 53
    SynthVoice = 54
    OrchestraHit = 55
    Trumpet = 56
    Trombone = 57
    Tuba = 58
    MutedTrumpet = 59
    FrenchHorns = 60
    BrassSection = 61
    SynthBrass1 = 62
    SynthBrass2 = 63
    SopranoSax = 64
    AltoSax = 65
    TenorSax = 66
    BaritoneSax = 67
    Oboe = 68
    EnglishHorn = 69
    Bassoon = 70
    Clarinet = 71
    Piccolo = 72
    Flute = 73
    Recorder = 74
    PanFlute = 75
    BottleChiff = 76
    Shakuhachi = 77
    Whistle = 78
    Ocarina = 79
    SquareLead = 80 
    SawWave = 81
    CalliopeLead = 82
    ChifferLead = 83
    Charang = 84
    SoloVox = 85
    FifthSawtoothWave = 86
    BassAndLead = 87
    Fantasia = 88
    WarmPad = 89
    Polysynth = 90
    SpaceVoice = 91
    BowedGlass = 92
    MetalPad = 93
    HaloPad = 94
    SweepPad = 95
    IceRain = 96
    Soundtrack = 97
    Crystal = 98
    Atmosphere = 99
    Brightness = 100
    Goblin = 101
    EchoDrops = 102
    StarTheme = 103
    Sitar = 104
    Banjo = 105
    Shamisen = 106
    Koto = 107
    Kalimba = 108
    BagPipe = 109
    Fiddle = 110
    Shenai = 111
    TinkerBell = 112
    Agogo = 113
    SteelDrums = 114
    Woodblock = 115
    TaikoDrum = 116
    MelodicTom = 117
    SynthDrum = 118
    ReverseCymbal = 119
    FretNoise = 120
    BreathNoise = 121
    SeaShore = 122
    BirdTweet = 123
    Telephone = 124
    Helicopter = 125
    Applause = 126
    GunShot = 127

    async def __call__(
            self,
            freq: Number | list[Number],
            velocity: int | list[int],
            duration: float,
            delay: float = 0,
        ):
        if isinstance(freq, Number):
            await synth.play(self, freq, velocity, duration, delay)
        else:
            await synth.play_chord(self, freq, velocity, duration, delay)


class PercussiveInstrument(Enum):
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

    # This naive interface does not enable "muffling" or "muting" of the instrument. TODO: improve
    async def __call__(self, velocity: int, delay: float = 0):
        if delay > 0:
            await asyncio.sleep(delay)
        output.send(mido.Message('note_on', channel=9, note=self.value, velocity=velocity))
