import curses
from curses import wrapper
import time
# import grid


def loop(stdscr, window, width, height):
    key = None
    y = 0
    x = 0

    while key != curses.KEY_BACKSPACE and key != ord('q'):
        key = window.getch()

        window.addch(y, x, ord(' '))

        if key == curses.KEY_DOWN:
            y = min(y + 1, height - 1)
        elif key == curses.KEY_RIGHT:
            x = min(x + 1, width - 1)
        elif key == curses.KEY_LEFT:
            x = max(0, x - 1)
        elif key == curses.KEY_UP:
            y = max(0, y - 1)

        for m in range(2, 40, 4):
            for n in range(4, 100, 1):
                window.addch(m, n, curses.ACS_S7)

        for n in range(4, 100, 8):
            for m in range(2, 40, 1):
                window.addch(m, n, ord('|'))

        window.addch(y, x, curses.ACS_S7)
        # stdscr.refresh()
        time.sleep(0.1)

def main():
    # stdscr.clear()
    
    stdscr = curses.initscr()
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    window = curses.newwin(sh, sw, 0, 0)
    window.keypad(1)
    window.timeout(100)

    loop(stdscr, window, sw, sh)

    curses.endwin()

main()

# quit()

# wrapper(main)
