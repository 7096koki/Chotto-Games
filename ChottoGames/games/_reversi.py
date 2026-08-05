import random
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from lib import screen, controls

INFO = {
    "title": "Reversi",
    "rule": "hikkurikaesite asobu teiban board game.",
    "controls": "↑↓←→: cursor idou | Enter: tama wo oku"
}

SIZE = 8
BLACK = "●"
WHITE = "◯"
stage = [["." for _ in range(8)] for _ in range(8)]

# 初期配置
stage[3][3] = WHITE
stage[4][4] = WHITE
stage[3][4] = BLACK
stage[4][3] = BLACK

def show_stage(x, y):
    screen.clear()
    for r, row in enumerate(stage):
        for c, cell in enumerate(row):
            if r == y and c == x:
                print(f"\033[7m{cell}\033[0m", end=" ")
            else:
                print(cell, end=" ")
        print()

def cpu_put():
    while True:
            cx = random.randint(0, SIZE - 1)
            cy = random.randint(0, SIZE - 1)
            
            if stage[cy][cx] == ".":
                stage[cy][cx] = WHITE
                break

def reverse(px, py, turn):
    is_end = False
    ix = px
    iy = py
    r = 0
    while (not is_end) or ix < SIZE - 1:
        ix += 1
        if stage[iy][ix] == turn:
            stage[iy][px:ix] =list(turn * (ix - px))
            break

def main():
    global x, y
    x, y = 3, 3  # 初期カーソル位置

    while True:
        show_stage(x, y)

        key = controls.readkey()

        match key:
            case "DOWN":
                y = min(SIZE - 1, y + 1)
            case "UP":
                y = max(0, y - 1)
            case "LEFT":
                x = max(0, x - 1)
            case "RIGHT":
                x = min(SIZE - 1, x + 1)
            case "ENTER":
                if stage[y][x] == ".":
                    stage[y][x] = BLACK
                    reverse(x, y, BLACK)



if __name__ == "__main__":
    main()