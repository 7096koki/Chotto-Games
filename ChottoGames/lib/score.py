import json
import os
import inspect

def save(level, new_score, user_data1=None, user_data2=None):
    save_file_path = "score.json"
    game_name = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]

    if os.path.exists(save_file_path):
        with open(save_file_path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    else:
        all_data = {}

    if game_name not in all_data:
        all_data[game_name] = {}

    level_str = str(level)
    if level_str not in all_data[game_name]:
        all_data[game_name][level_str] = []

    all_data[game_name][level_str].append(new_score)
    all_data[game_name][level_str].sort()

    all_data[game_name][level_str] = all_data[game_name][level_str][:10]

    with open(save_file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)