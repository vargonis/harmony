import curses
from pynput.keyboard import Key, Controller
from threading import Thread
import time

from microtonal.instruments import MelodicInstrument, PercussiveInstrument
from microtonal.greek import GreekMode
from microtonal.players import Band, TonalPlayer, RythmicPlayer, Pattern


band = Band()

drum_patterns = [
    Pattern(
        8,
        [(0,1), (1,1), (1.5,1), (3,1), (5,1), (6.5,1), (7,1)],
        [[0],   [1],   [0],     [1],   [1],   [0],     [1]],
    ),
    Pattern(
        8,
        [(0,1), (1,1), (1.5,1), (2,1), (3,1), (4,1), (4.5,1), (5,1), (6,1), (6.5,1), (7,1)],
        [[0,2], [1,2], [0],     [2],   [1,2], [2],   [0],     [1,2], [0,2], [0],     [1,2]],
    ),
]
drum_p = 0
organ_patterns = [
    Pattern(8, [(0, 6), (6, 2)], [[-3, 0, 2], [-1, 1, 4]]),
    # Pattern(8, [(0, 3), (3, 1)], [[0, 2, 4], [0, 3, 5]]),
]

band["drummer"] = RythmicPlayer(
    100, drum_patterns[drum_p],
    [PercussiveInstrument.AcousticBassDrum, PercussiveInstrument.AcousticSnare, PercussiveInstrument.RideCymbal1],
)
band["drummer"].play_in_loop(3, band.loop)
band["organ"] = TonalPlayer(
    100, organ_patterns[0],
    300, GreekMode.MAJOR, MelodicInstrument.PercussiveOrgan,
)
band["organ"].play_in_loop(3, band.loop)

measure = 3
messages = []

def measure_tick():
    keyboard = Controller()
    stop = False
    while not stop:
        band.play(measure)
        try:
            while True:
                k = messages.pop()
                if k == 27: # "esc"
                    stop = True
        except:
            pass
        # A message to curses, so it can refresh the window:
        keyboard.press(Key.enter); keyboard.release(Key.enter)
        time.sleep(measure)


def main(win: curses.window):
    global drum_p
    tick_thread = Thread(target=measure_tick)
    tick_thread.start()
    # win.nodelay(True)
    while not 27 in messages: # 27 is "esc"
        win.clear()
        win.addstr(f"Pressed keys: {messages}")
        k = win.getch()
        if k != 10: # an "enter" is just a message from `measure_tick`, to clear the window
            messages.append(k)
            # here, code to handle the key press too (updates to the band state for the next tick):
            if chr(k) == 'd':
                print("drummer")
                drum_p = (drum_p + 1) % len(drum_patterns)
                band["drummer"].pattern = drum_patterns[drum_p]
    tick_thread.join()

curses.wrapper(main)

messages.append(27)

