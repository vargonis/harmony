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
    handlers: dict[str, callable] = field(default_factory=dict)

    def __post_init__(self):
        def quit():
            self.stop = True
        self.handlers["quit"] = quit

    def tick(self):
        while not self.stop:
            self.band.play(self.tempo)
            time.sleep(self.tempo)

    def start(self):
        self.stop = False
        self.messages = ["start"]
        tick_thread = Thread(target=self.tick)
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
                    win.addstr(str(e))
        curses.wrapper(main)
        tick_thread.join()
