import json
import os
import inspect

SAVE_FILE_PATH = "score.json"

def save(level, new_score, *user_data):
    # 呼び出し元のファイル名からゲーム名を取得
    game_name = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]

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

    # スコアデータ構造: [スコア, 追加データ1, 追加データ2, ...]
    # user_dataはタプルなので、リストに展開して結合する
    score_entry = [new_score] + list(user_data)
    all_data[game_name][level_str].append(score_entry)

    # ソート（リストの最初の要素である「スコア」を基準に自動で昇順ソートされる！）
    all_data[game_name][level_str].sort(key=lambda x: x[0])

    # 上位10件をキープ
    all_data[game_name][level_str] = all_data[game_name][level_str][:10]

    with open(SAVE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)


def load(game_name, level):
    """
    引数のゲームとレベルに応じたランキング（最大10件）を返す。
    データが存在しない場合は空のリスト [] を返す。
    """
    if not os.path.exists(SAVE_FILE_PATH):
        return []

    with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
        all_data = json.load(f)

    level_str = str(level)
    
    # 指定されたゲームやレベルのデータがない場合は空のリストを安全に返す
    return [item for sublist in (all_data.get(game_name, {}).get(level_str, [])) for item in sublist]