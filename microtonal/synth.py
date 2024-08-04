from dataclasses import dataclass
from typing import TypeAlias, Iterable
from numbers import Number
import mido
import math

from .output import output
from .program import Program

NoteId: TypeAlias = tuple[int, int]


# NOTE: the class below is thread safe, because it only relies on list's pop and append.

@dataclass
class Synth:
    channels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15] # channel 9 is for percussion

    def note_on(self, program: Program, freq: Number, velocity: int) -> NoteId:
        # the return value functions as an id, to turn the note off later (thus liberating its channel)
        try:
            channel = self.channels.pop()
        except:
            raise Exception('No channels available')
        output.send(mido.Message('program_change', channel=channel, program=program.value))
        midi_note = int(69 + 12 * math.log2(freq / 440.0))
        note_frequency = 440.0 * pow(2.0, (midi_note - 69) / 12.0)
        pitch_bend = int(8191 * math.log2(freq / note_frequency) * 6)
        output.send(mido.Message('pitchwheel', channel=channel, pitch=pitch_bend))
        output.send(mido.Message('note_on', channel=channel, note=midi_note, velocity=velocity))
        return (channel, midi_note)

    def note_off(self, nid: NoteId) -> None:
        output.send(mido.Message('note_off', channel=nid[0], note=nid[1]))
        self.channels.append(nid[0])

    def chord_on(self, program: Program, base: float, chord: Iterable[Number], velocities: int | Iterable[int]) -> list[NoteId]:
        if isinstance(velocities, int):
            velocities = [velocities] * len(chord)
        # print(chord, velocities)
        note_ids = []
        for shift, velocity in zip(chord, velocities):
            note_ids.append(self.note_on(program, base * shift, velocity))
        return note_ids

    def chord_off(self, note_ids: list[NoteId]) -> None:
        for note_id in note_ids:
            self.note_off(note_id)
