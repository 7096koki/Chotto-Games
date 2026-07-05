import random
import sys
import readchar

INFO ={
    "title": "Guess the Number",
    "rule": "goku hutu no kazuate game.",
    "controls": "number key: kazu nyuryoku | Enter: kettei | ↑↓: cursor idou"
}

def main():
    count = 0
    n = random.randint(1, max_n)
    history = []  # 過去の入力を保存するリスト
    history_index = -1  # 今、履歴のどこを見ているか（-1は未選択）

    while True:
        # 自作の文字入力バッファ
        current_input = ""
        cursor_idx = 0  # ★【重要】ここで毎回、カーソル位置を0に初期化する！
        print("\033[3;1H\033[0Kanswer: ", end="", flush=True)

        # Enterが押されるまで1文字ずつ入力を受け付けるループ
        while True:
            key = readchar.readkey()

            if key == readchar.key.ENTER:
                if current_input.isdigit():  # 数字が入っていれば確定
                    break
                elif len(current_input) == 0:
                    continue  # 空っぽなら無視

            elif key == readchar.key.UP:
                # 上矢印：過去の履歴を古い順に（または最新から）遡る
                if len(history) > 0:
                    history_index = min(history_index + 1, len(history) - 1)
                    current_input = str(history[-(history_index + 1)])
                    cursor_idx = len(
                        current_input
                    )  # ★カーソルを文字の末尾に移動

            elif key == readchar.key.DOWN:
                # 下矢印：履歴を戻す
                if history_index > 0:
                    history_index -= 1
                    current_input = str(history[-(history_index + 1)])
                    cursor_idx = len(
                        current_input
                    )  # ★カーソルを文字の末尾に移動
                else:
                    history_index = -1
                    current_input = ""  # 一番下まで戻ったら空にする
                    cursor_idx = 0  # ★文字が空なのでカーソルも0

            elif key == readchar.key.LEFT:
                # 左矢印：カーソルを左に移動（0未満にはならない）
                cursor_idx = max(0, cursor_idx - 1)

            elif key == readchar.key.RIGHT:
                # 右矢印：カーソルを右に移動（現在の文字数を超えない）
                cursor_idx = min(len(current_input), cursor_idx + 1)

            elif key in (readchar.key.BACKSPACE, "\x7f"):
                # カーソルより左の文字を消す
                if cursor_idx > 0:
                    current_input = (
                        current_input[: cursor_idx - 1]
                        + current_input[cursor_idx:]
                    )
                    cursor_idx -= 1

            elif key.isdigit():
                # すでに文字があって、カーソルが文字の「途中」を指している場合は上書き、
                # カーソルが末尾（=文字数と同じ）なら末尾に追加する
                if cursor_idx < len(current_input):
                    # 特定の桁をピンポイントで上書き（置換）
                    current_input = (
                        current_input[:cursor_idx]
                        + key
                        + current_input[cursor_idx + 1 :]
                    )
                else:
                    # 通常通りの追加
                    current_input += key

                # 1文字入力されたのでカーソルを右に1つ進める
                cursor_idx += 1

            # --- 💡 Linuxのエスケープシーケンスで画面を再描画 ---
            # 1. 3行目のスタート位置に戻って、行をクリアして最新の状態を描画
            print(f"\033[3;1H\033[0Kanswer: {current_input}", end="")
            # 2. 「answer: 」の文字数（8文字）＋現在のカーソル位置に、端末のカーソルを正確にジャンプさせる！
            actual_col = 8 + cursor_idx + 1
            print(f"\033[3;{actual_col}H", end="", flush=True)

        # Enterが押された後の処理
        answer = int(current_input)
        history.append(answer)  # 履歴に追加
        history_index = -1  # 履歴の選択状態をリセット
        count += 1

        print("\033[4;1H\033[0K")
        if answer < n:
            print("\033[4;1HIt's bigger number(+)")
        elif answer > n:
            print("\033[4;1HIt's smaller number(-)")
        elif answer == n:
            print(f"Correct answer after {count} time!")
            input("Press any key to return to menu...")
            break  # ゲーム終了してメニューへ戻る

        # ★ヒントの判定
        if level > 1 and abs(n - answer) < (max_n / 10):
            hint_range = 10 ** (level - 1)
            print(f"gosa ha \u00b1 {hint_range}")  # \u00b1 は半角の「±」記号

if __name__ == "__main__":
    level = int(sys.argv[1])
    max_n = 10**level
    print("1 ~ {max_n}")
    main()