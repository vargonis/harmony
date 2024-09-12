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
    n_beats: int # NOTE: consistency between this and the n_beats attribute that each of the band players patterns have is not required. What is required (but not enforced; expect unexpected behaviour) is that the n_beats attribute of the band be greater than or equal to the n_beats attribute of each of the players.
    tempo: float
    handlers: dict[str, callable] = field(default_factory=dict)

    def __post_init__(self):
        def quit():
            self.stop = True
        self.handlers["quit"] = quit

    def main_loop(self):
        beat = 0
        events = {i: list() for i in range(self.n_beats)}
        events[0].extend(self.band.keys())
        def tick():
            nonlocal beat, events
            beat_events = events[beat].copy()
            events[beat].clear()
            for player in beat_events:
                self.band.play(player, self.tempo)
                events[(beat + self.band[player].pattern.n_beats) % self.n_beats].append(player)
            beat = (beat + 1) % self.n_beats
        while not self.stop:
            tick()
            time.sleep(self.tempo)

    def start(self):
        self.stop = False
        self.messages = ["start"]
        main_thread = Thread(target=self.main_loop)
        main_thread.start()
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
        main_thread.join()
