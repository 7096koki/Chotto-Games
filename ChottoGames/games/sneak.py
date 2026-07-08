import sys
import os
import time
import threading
import random

import readchar

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from lib import screen

SIZE = 17

stage = [["." for _ in range(17)] for _ in range(15)]

global direction
direction = "right"

def show_stage():
    screen.clear()
    for row in stage:
        for cell in row:
            print(cell, end=" ")
        print()
    
    print(direction) # pyright: ignore[reportUndefinedVariable]

def key_input():
    global direction
    while True:
        key = readchar.readkey()

        match key:
            case readchar.key.DOWN:
                if direction != "up":
                    direction = "down"
            case readchar.key.UP:
                if direction != "down":
                    direction = "up"
            case readchar.key.LEFT:
                if direction != "right":
                    direction = "left"
            case readchar.key.RIGHT:
                if direction != "left":
                    direction = "right"

def main():
    global direction
    direction = "right"

    # 1. 最初から3マス分の座標を仕込んでおく（右に進むので、左に胴体を伸ばしておく）
    # [頭, 胴体1, 胴体2] の順番
    snake = [[8, 8], [7, 8], [6, 8]]

    # 最初にステージにヘビを配置しておく
    for pos in snake:
        stage[pos[1]][pos[0]] = "#"

    listener_thread = threading.Thread(target=key_input, daemon=True)
    listener_thread.start()

    while True:
        show_stage()

        # 次の頭の座標を計算
        head_x, head_y = snake[0]  # いまの頭の場所

        match direction:
            case "down":
                head_y += 1
            case "up":
                head_y -= 1
            case "left":
                head_x -= 1
            case "right":
                head_x += 1

        # 壁の判定
        if 0 <= head_x < SIZE and 0 <= head_y < len(stage):
            # 新しい頭の座標をリストの【先頭】に突っ込む
            snake.insert(0, [head_x, head_y])

            # 一番古い【お尻の座標】を抜き取って、ステージから消す
            tail = snake.pop()
            stage[tail[1]][tail[0]] = "."

            # 新しい頭をステージに描き込む
            stage[head_y][head_x] = "#"
        else:
            print("GAME OVER (Hit Wall!)")
            readchar.readkey()

        time.sleep(0.1)
        

                

if __name__ == "__main__":
    main()