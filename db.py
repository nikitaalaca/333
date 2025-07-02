import json
from datetime import datetime, timedelta

DB_FILE = "storage.json"
V2RAY_FILE = "users.json"

def load_data():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_keys():
    try:
        with open(V2RAY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_keys(data):
    with open(V2RAY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_subscription(user_id):
    data = load_data()
    ts = data.get(user_id, {}).get("sub_until")
    if ts:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    return None

def set_subscription(user_id, username, days, trial=False):
    data = load_data()
    expire = datetime.utcnow() + timedelta(days=days)
    data[user_id] = {
        "username": username,
        "sub_until": expire.strftime("%Y-%m-%d %H:%M:%S"),
        "trial": trial
    }
    save_data(data)
    return expire

def has_used_trial(user_id):
    data = load_data()
    return data.get(user_id, {}).get("trial", False)

def deactivate_expired_users():
    data = load_data()
    now = datetime.utcnow()
    for item in data:
    uid = item.get("user_id") or item.get("id")
    if not uid:
        continue
        sub_until = datetime.strptime(data[uid]["sub_until"], "%Y-%m-%d %H:%M:%S")
        if sub_until < now:
            del data[uid]
    save_data(data)

def get_all_users():
    return load_data()

def delete_user(user_id):
    data = load_data()
    keys = load_keys()
    if user_id in data:
        del data[user_id]
    if user_id in keys:
        del keys[user_id]
    save_data(data)
    save_keys(keys)

def update_v2ray_key(user_id, key):
    keys = load_keys()
    keys[user_id] = key
    save_keys(keys)

def get_v2ray_key(user_id):
    keys = load_keys()
    return keys.get(user_id)

def is_admin(user_id):
    return str(user_id) in load_data().get("admins", [])

def is_moderator(user_id):
    return str(user_id) in load_data().get("moderators", [])

def add_admin(user_id):
    data = load_data()
    if "admins" not in data:
        data["admins"] = []
    if user_id not in data["admins"]:
        data["admins"].append(user_id)
    save_data(data)

def remove_admin(user_id):
    data = load_data()
    if "admins" in data and user_id in data["admins"]:
        data["admins"].remove(user_id)
    save_data(data)
