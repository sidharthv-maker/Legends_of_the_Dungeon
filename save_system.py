import json
import os
from data import SAVE_FILE
from models import Player
def save_game(player):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(player.to_dict(), f, indent=4)
    print("\nGame saved successfully.")
def load_game():
    if not os.path.exists(SAVE_FILE):
        print("\nNo save file found.")
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        player = Player.from_dict(data)
        print("\nSave loaded successfully.")
        return player
    except (json.JSONDecodeError, KeyError, TypeError):
        print("\nSave file is corrupted or invalid.")
        return None
def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("\nSave file deleted.")
    else:
        print("\nNo save file exists.")