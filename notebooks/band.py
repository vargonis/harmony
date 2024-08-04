from dataclasses import dataclass
from fractions import Fraction
from threading import Thread
import sched, time
import blinker

from microtonal.synth import Synth
from microtonal.program import Program
from microtonal.percussion import Percussion
from microtonal.greek import GreekChord, GreekScale

synth = Synth()


@dataclass
class Pattern:
    rythm: list[tuple[int, int]] # start/stop beat indices on which clusters are to be played
    clusters: list[list[int]] # "chords" of the current mode (or percussions in the kit, if the player is rythmic) to be played, must have same length as `rythm`
    # dynamics: list[list[int]] # relative increase/decrease of volume on each note. Leave it out, for now

@dataclass
class Player:
    vol: int
    pattern: Pattern

@dataclass
class TonalPlayer(Player):
    tone: float # base frequency
    mode: list[Fraction] # harmonic scale
    program: Program # midi terminology: the instrument's program number

    def play(self, lapse: float):
        s = sched.scheduler(time.time, time.sleep)
        n = len(self.pattern.rythm)
        def play_note(i, duration):
            nid = synth.note_on(self.program, self.tone * self.mode[i], self.vol)
            s.enter(duration, 1, synth.note_off, argument=(nid,))
        for cluster, (start, stop) in zip(self.pattern.clusters, self.pattern.rythm):
            for i in cluster:
                s.enter(start * lapse / n, 1, play_note, argument=(i, (stop - start) * lapse / n))
        thread = Thread(target=s.run)
        return thread.start()


@dataclass
class RythmicPlayer(Player):
    kit: list[Percussion] # percussion instruments

    def play(self, lapse: float):
        s = sched.scheduler(time.time, time.sleep)
        n = len(self.pattern.rythm)
        for cluster, (beat, _) in zip(self.pattern.clusters, self.pattern.rythm):
            for i in cluster:
                s.enter(beat * lapse / n, 1, self.kit[i], argument=(self.vol,))
        thread = Thread(target=s.run)
        return thread.start()


pattern = Pattern([(0, 0), (1, 1), (2, 2), (3, 3)], [[0, 2], [1, 2], [0, 2], [1, 2]])
drummer = RythmicPlayer(100, pattern, [Percussion.AcousticBassDrum, Percussion.AcousticSnare, Percussion.RideCymbal1])
drummer.play(1)

pattern = Pattern([(0, 3), (3, 1)], [[1, 3, 5], [1, 4, 5]])
organ = TonalPlayer(100, pattern, 200, GreekScale.MAJOR.value, Program.PercussiveOrgan)
organ.play(1)

measure = blinker.signal("measure")
measure.connect(drummer.play)
measure.connect(organ.play)

for _ in range(2):
    measure.send(1.2)
    time.sleep(1.2)


#%%
import curses
import os

def main(win):
    win.nodelay(True)
    win.clear()                
    win.addstr("Detected key:")
    key = ""
    while 1:          
        try:                 
            key = win.getkey()         
            win.clear()                
            win.addstr("Detected key:")
            win.addstr(str(key)) 
            if key == os.linesep:
                break           
        except Exception as e:
            # No input   
            pass         

curses.wrapper(main)