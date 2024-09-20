from dataclasses import dataclass, field
from threading import Thread
import curses
from curses import ascii
import time

from .players import Band

curses.set_escdelay(1)


@dataclass
class App:
    band: Band
    tempo: float
    handlers: dict[str, callable] = field(default_factory=dict) # defines how the app will react to user input

    def __post_init__(self):
        self.n_beats = 0
        def quit():
            self.stop = True
        self.handlers["quit"] = quit # so, input "quit" to stop the app

    def tick_loop(self):
        beat: int = 0
        events: list[int, str] = {i: list() for i in range(self.n_beats)} # We keep a list of players to be triggered on each beat of the current measure. TODO: it might be tempting to consider using floats instead of integers, to allow for triggering players in between beats (we use this dictionary just to allow for band players with different n_beats each, thus needing to re-start them at shifting beats, as the loop proceeds). This level of generality does not seem to be musically necessary.
        events[0].extend(self.band.keys())
        def tick():
            nonlocal beat, events
            beat_events = events[beat].copy()
            events[beat].clear()
            for player in beat_events:
                self.band.play(player, self.tempo)
                events[(beat + self.band[player].part.n_beats) % self.n_beats].append(player)
            beat = (beat + 1) % self.n_beats
        while not self.stop:
            tick()
            time.sleep(self.tempo)

    def start(self):
        self.n_beats = max([p.part.n_beats for p in self.band.values()])
        self.stop = False
        self.messages = ["start"] # no particular use for this, it just feels nice to log the start of the app
        tick_thread = Thread(target=self.tick_loop)
        tick_thread.start()
        def main(win: curses.window):
            win.clear()
            while self.messages[-1] != "quit":
                current_message = ""
                win.addstr(">>> ")
                k = win.getch()
                while k != 10: # enter
                    if k == 127: # backspace
                        if len(current_message) > 0:
                            current_message = current_message[:-1]
                            y, x = win.getyx()
                            win.move(y, x - 1)
                            win.clrtoeol()
                    elif ascii.isalnum(k) or ascii.isspace(k):
                        current_message += chr(k)
                        win.addstr(chr(k))
                    k = win.getch()
                self.messages.append(current_message)
                y, x = win.getyx()
                win.move(y + 1, 0)
                try:
                    command, *args = self.messages[-1].split()
                    handler = self.handlers.get(command, None)
                    if handler:
                        handler(*args)
                except Exception as e:
                    win.addstr(str(e) + '\n')
        curses.wrapper(main)
        tick_thread.join()
