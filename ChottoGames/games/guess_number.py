import random
import sys
import time
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from lib import score, controls

INFO = {
    "title": "guess_number",
    "rule": "goku hutu no kazuate game desu.",
    "controls": "number key: kazu nyuryoku | Enter: kettei | ↑↓: rireki shutoku | Space: Hint no hyouji",
    "max_level": 255
}


def main():
    global count
    global hint_count
    count = 0
    n = random.randint(min_n, max_n)
    history = []  # 過去の入力を保存するリスト
    history_index = -1  # 今、履歴のどこを見ているか（-1は未選択）
    hint_count = 0

    # 最小レンジと最大レンジの初期値を、ゲームの限界値にしておく
    min_range = min_n
    max_range = max_n

    while True:
        print("\033[6;1H\033[0K" + "-" * 40)
        print(f"\033[7;1H\033[0K{INFO["controls"]}")

        # 自作の文字入力バッファ
        current_input = ""
        cursor_idx = 0  # ここで毎回、カーソル位置を0に初期化
        print("\033[3;1H\033[0Kanswer: ", end="")

        # Enterが押されるまで1文字ずつ入力を受け付けるループ
        while True:
            key = controls.readkey()

            match key:
                case "ENTER":
                    if current_input.isdigit():  # 数字が入っていれば確定
                        break
                    elif len(current_input) == 0:
                        continue  # 空っぽなら無視

                case "UP":
                    # 上矢印：過去の履歴を最新から遡る
                    if len(history) > 0:
                        history_index = min(history_index + 1, len(history) - 1)
                        current_input = str(history[-(history_index + 1)])
                        cursor_idx = len(current_input)

                case "DOWN":
                    # 下矢印：履歴を戻す
                    if history_index > 0:
                        history_index -= 1
                        current_input = str(history[-(history_index + 1)])
                        cursor_idx = len(current_input)
                    else:
                        history_index = -1
                        current_input = ""
                        cursor_idx = 0

                case "LEFT":
                    cursor_idx = max(0, cursor_idx - 1)

                case "RIGHT":
                    cursor_idx = min(len(current_input), cursor_idx + 1)

                case "SPACE":
                    # 【修正】まだ確定前のanswerは使えないので、現在の入力文字(あれば)か履歴の最後を使う
                    if LEVEL != 1:
                        print(
                            f"\033[5;1H\033[0KCurrent Range: {min_range} ~ {max_range}"
                        )
                        hint_count += 1
                        time.sleep(1.5)
                        print("\033[5;1H\033[0K")  # 表示後にヒント行を消去
                    else:
                        print("\033[5;1H\033[0KHint: None")
                        time.sleep(1.0)
                        print("\033[5;1H\033[0K")

                case "BACKSPACE":
                    if cursor_idx > 0:
                        current_input = (
                            current_input[: cursor_idx - 1]
                            + current_input[cursor_idx:]
                        )
                        cursor_idx -= 1

                case _ if key.isdigit():
                    if cursor_idx < len(current_input):
                        current_input = (
                            current_input[:cursor_idx]
                            + key
                            + current_input[cursor_idx + 1 :]
                        )
                    else:
                        current_input += key
                    cursor_idx += 1

            # --- エスケープシーケンスで画面を再描画 ---
            print(f"\033[3;1H\033[0Kanswer: {current_input}", end="")
            actual_col = 8 + cursor_idx + 1
            print(f"\033[3;{actual_col}H", end="", flush=True)

        # Enterが押された後の処理
        answer = int(current_input)
        history.append(answer)
        history_index = -1
        count += 1

        # 【修正】数当てゲームの範囲絞り込みロジック
        if answer < n:
            print("\033[4;1H\033[0KIt's bigger number(+)")
            min_range = max(min_range, answer + 1)  # 最小値を更新
        elif answer > n:
            print("\033[4;1H\033[0KIt's smaller number(-)")
            max_range = min(max_range, answer - 1)  # 最大値を更新
        elif answer == n:
            print(
                f"\033[4;1H\033[0KCorrect answer after {count} time! (Hint used: {hint_count})"
            )
            print("Press any key to return to menu...")
            controls.readkey()
            break


if __name__ == "__main__":
    LEVEL = int(sys.argv[1])
    max_n = 10**LEVEL
    min_n = max_n // 10
    print(f"Lv.{LEVEL}: {min_n} ~ {max_n}")
    main()
    score.save("guess_number", LEVEL, count, hint_count)