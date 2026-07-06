import json
import os

SAVE_FILE_PATH = "score.json"


# 【修正】第一引数に game_name を手動で渡すように変更！
def save(game_name, level, new_score, *option_data):
    if os.path.exists(SAVE_FILE_PATH):
        with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    else:
        all_data = {}

    if game_name not in all_data:
        all_data[game_name] = {}

    level_str = str(level)
    if level_str not in all_data[game_name]:
        all_data[game_name][level_str] = []

    score_entry = [new_score] + list(option_data)
    all_data[game_name][level_str].append(score_entry)

    # 昇順ソート
    all_data[game_name][level_str].sort(key=lambda x: x[0])
    # 10個までのデータに絞りたい場合は下のコードを追加
    # all_data[game_name][level_str] = all_data[game_name][level_str][:10]

    with open(SAVE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)


def load(game_name, level):
    if not os.path.exists(SAVE_FILE_PATH):
        return []

    with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
        all_data = json.load(f)

    level_str = str(level)
    raw_records = all_data.get(game_name, {}).get(level_str, [])

    formatted_ranking = []

    # raw_records は [[11, 0], [12, 1]] のようなリストのリスト
    for record in raw_records:
        score_val = record[0]  # 最初の要素は必ずメインスコア（手数など）

        # オプションデータ（ヒントなど）があるかチェック
        if len(record) > 1:
            hint_val = record[1]
            # ローマ字の世界観に合わせて、文字列を作成
            formatted_ranking.append(f"{score_val} (Hint count: {hint_val})")
        else:
            # マインスイーパーなど、スコア（タイムなど）だけのとき
            formatted_ranking.append(f"{score_val / 1000}s")

    # 例: ["11 tewaza (Hint: 0)", "12 tewaza (Hint: 1)"] というリストが返る
    return formatted_ranking