import os
import random
import sys
import threading
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from lib import controls, score, screen

INFO = {
    "title": "sneak",
    "rule": "yajirushi de hebi wo ayatutte esa wo tabesaseyou!",
    "controls": "↑↓←→: houkou tenkan",
    "max_level": 9
}

SIZE = {"x": 17, "y": 15}

stage = [
    ["\x1b[38;5;242m.\x1b[0m" for _ in range(SIZE["x"])]
    for _ in range(SIZE["y"])
]

direction = "right"
is_running = True  # スレッド停止用フラグ


def show_stage():
    screen.clear()
    for row in stage:
        for cell in row:
            print(cell, end=" ")
        print("\r")


def key_input():
    global direction, is_running
    # ゲーム実行中のみキー監視を行う（メニューに戻った後の画面崩れ防止）
    while is_running:
        key = controls.readkey()

        match key:
            case "DOWN":
                if direction != "up":
                    direction = "down"
            case "UP":
                if direction != "down":
                    direction = "up"
            case "LEFT":
                if direction != "right":
                    direction = "left"
            case "RIGHT":
                if direction != "left":
                    direction = "right"


def spawn_food(snake):
    """ヘビの体以外の空いているマスにエサを置く"""
    while True:
        fx = random.randint(0, SIZE["x"] - 1)
        fy = random.randint(0, SIZE["y"] - 1)
        if [fx, fy] not in snake:
            stage[fy][fx] = "\033[31m@\033[0m"
            return fx, fy


def main():
    global direction, is_running
    direction = "right"
    is_running = True

    # コマンドライン引数からレベル（1〜9）を取得（デフォルトはレベル 1）
    level_val = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    level_val = max(1, min(9, level_val))  # 1〜9の範囲に収める

    speed_map = {
        1: 1.0,
        2: 0.6,
        3: 0.35,
        4: 0.2,
        5: 0.12,
        6: 0.08,
        7: 0.05,
        8: 0.032,
        9: 0.021,  # 限界爆速モード！
    }
    sleep_time = speed_map.get(level_val, 1.0)

    # [頭, 胴体1, 胴体2]
    snake = [[8, 8], [7, 8], [6, 8]]

    for pos in snake:
        stage[pos[1]][pos[0]] = "\033[32m#\033[0m"

    # 最初のエサを配置
    food_x, food_y = spawn_food(snake)

    # 1. 最初にステージを描画
    show_stage()
    print("Press Any Key to Start...\r")

    # 2. スタート待ち（スレッド起動前に1回だけ取得）
    controls.readkey()

    # 3. キー監視スレッドを起動
    listener_thread = threading.Thread(target=key_input, daemon=True)
    listener_thread.start()

    while True:
        show_stage()

        head_x, head_y = snake[0]

        match direction:
            case "down":
                head_y += 1
            case "up":
                head_y -= 1
            case "left":
                head_x -= 1
            case "right":
                head_x += 1

        # 1. 壁判定
        if not (0 <= head_x < SIZE["x"] and 0 <= head_y < SIZE["y"]):
            print("\r\nGAME OVER (Hit Wall!)\r")
            break

        # 2. 自分の体への衝突判定
        if [head_x, head_y] in snake[:-1]:
            print("\r\nGAME OVER (Hit Yourself!)\r")
            break

        # 3. エサを食べた判定
        if head_x == food_x and head_y == food_y:
            snake.insert(0, [head_x, head_y])
            stage[head_y][head_x] = "\033[32m#\033[0m"
            food_x, food_y = spawn_food(snake)
        else:
            tail = snake.pop()
            stage[tail[1]][tail[0]] = "\x1b[38;5;242m.\x1b[0m"
            snake.insert(0, [head_x, head_y])
            stage[head_y][head_x] = "\033[32m#\033[0m"

        time.sleep(sleep_time)

    # ゲーム終了に伴いキー監視スレッドを停止
    is_running = False

    # スコアの処理
    final_score = len(snake)

    print("-" * 30 + "\r")
    print(f"SCORE: {final_score}\r")

    score.save("sneak", level_val, final_score)

    time.sleep(0.2)
    print("Press Enter key to return...\r")
    controls.readkey()

    # プロセスを確実に終了して親プロセス（メニュー）に復帰
    sys.exit(0)


if __name__ == "__main__":
    main()