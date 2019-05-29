import curses
import time

class Grid(object):
    def __init__(self, h=0, w=0):
        self.h = h
        self.w = w
        self.grid = [[None for _ in range(h)] for _ in range(w)]
        self.pos = [0, 0]

    def draw(self, window):
        pass

    def move_up(self):
        self.pos[1] = min(self.pos[1] + 1, self.h - 1)

    def move_down(self):
        self.pos[1] = max(self.pos[1] - 1, 0)

    def move_left(self):
        self.pos[0] = min(self.pos[0] + 1, self.w - 1)
    
    def move_right(self):
        self.pos[0] = max(self.pos[0] - 1, 0)

if __name__ == '__main__':
    pass