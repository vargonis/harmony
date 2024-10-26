import asyncio

from microtonal import synth
from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.harmony import Major, minor


asyncio.run(synth.play_hit(PercussiveInstrument.ChineseCymbal.value, 100))
asyncio.run(synth.play_note(MelodicInstrument.PercussiveOrgan.value, 300, 100, 1))
asyncio.run(synth.play_chord(MelodicInstrument.PercussiveOrgan.value, Major(3, 300), 100, 1))
asyncio.run(synth.play_chord(MelodicInstrument.YamahaGrandPiano.value, 100 * minor(3), 100, 1))
