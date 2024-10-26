from dataclasses import dataclass
from typing import Iterable
from numbers import Number
import math
import mido
import asyncio

# from .instruments import MelodicInstrument # circulariry
# from .events import Hit, Note, Chord # would introduce circularity

output = mido.open_output()


# NOTE: the class below is thread safe, because it only relies on list's pop and append.

@dataclass
class Synth:
    channels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15] # channel 9 is for percussion

    async def play_hit(
            self,
            instrument: int,
            velocity: int,
            delay: float = 0,
        ):
        # TODO: add support for muffling or muting (ie take into account the hit duration)
        if delay > 0:
            await asyncio.sleep(delay)
        output.send(mido.Message('note_on', channel=9, note=instrument, velocity=velocity))

    async def play_note(
            self,
            program: int,
            frequency: float,
            velocity: int,
            duration: float,
            delay: float = 0,
        ):
        if delay > 0:
            await asyncio.sleep(delay)
        try:
            channel = self.channels.pop()
        except:
            raise Exception('No channels available')
        output.send(mido.Message('program_change', channel=channel, program=program))
        midi_note = int(69 + 12 * math.log2(frequency / 440.0))
        tempered_frequency = 440.0 * pow(2.0, (midi_note - 69) / 12.0)
        pitch_bend = int(8191 * math.log2(frequency / tempered_frequency) * 6)
        output.send(mido.Message('pitchwheel', channel=channel, pitch=pitch_bend))
        output.send(mido.Message('note_on', channel=channel, note=midi_note, velocity=velocity))
        await asyncio.sleep(duration)
        output.send(mido.Message('note_off', channel=channel, note=midi_note))
        self.channels.append(channel)

    async def play_chord(
            self,
            program: int,
            frequencies: Iterable[Number],
            velocity: int,
            duration: float,
            delay: float = 0,
        ):
        if delay > 0:
            await asyncio.sleep(delay)
        await asyncio.gather(
            *[self.play_note(program, x, velocity, duration) for x in frequencies]
        )
