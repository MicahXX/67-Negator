import os, json

EXCLUSIONS_FILE = "exclusions.json"

def load_exclusions():
    if not os.path.exists(EXCLUSIONS_FILE):
        return {}
    with open(EXCLUSIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_exclusions(data):
    with open(EXCLUSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_guild_data(exclusions, guild_id: int):
    guild_id = str(guild_id)
    if guild_id not in exclusions:
        exclusions[guild_id] = {"users": [], "channels": []}
    return exclusions[guild_id]
