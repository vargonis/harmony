from dataclasses import dataclass
from typing import Iterable
from numbers import Number
import asyncio
import mido
import math

from . import output
from .instruments import MelodicInstrument


# NOTE: the class below is thread safe, because it only relies on list's pop and append.

@dataclass
class Synth:
    channels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15] # channel 9 is for percussion

    async def play(
            self,
            instrument: MelodicInstrument,
            freq: Number,
            velocity: int,
            duration: float,
            delay: float = 0,
        ):
        # the return value functions as an id, to turn the note off later (thus liberating its channel)
        if delay > 0:
            await asyncio.sleep(delay)
        try:
            channel = self.channels.pop()
        except:
            raise Exception('No channels available')
        output.send(mido.Message('program_change', channel=channel, program=instrument.value))
        midi_note = int(69 + 12 * math.log2(freq / 440.0))
        note_frequency = 440.0 * pow(2.0, (midi_note - 69) / 12.0)
        pitch_bend = int(8191 * math.log2(freq / note_frequency) * 6)
        output.send(mido.Message('pitchwheel', channel=channel, pitch=pitch_bend))
        output.send(mido.Message('note_on', channel=channel, note=midi_note, velocity=velocity))
        await asyncio.sleep(duration)
        output.send(mido.Message('note_off', channel=channel, note=midi_note))
        self.channels.append(channel)

    async def play_chord(
            self,
            instrument: MelodicInstrument,
            freqs: Iterable[Number],
            velocities: int | Iterable[int],
            duration: float,
            delay: float = 0,
        ):
        if isinstance(velocities, int):
            velocities = [velocities] * len(freqs)
        # print(chord, velocities)
        if delay > 0:
            await asyncio.sleep(delay)
        await asyncio.gather(*[self.play(instrument, freq, velocity, duration) for freq, velocity in zip(freqs, velocities)])
