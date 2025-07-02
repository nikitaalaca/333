import json
from datetime import datetime, timedelta

STORAGE_FILE = "storage.json"
ADMINS_FILE = "users.json"

def load_data():
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_subscription(user_id):
    data = load_data()
    sub = data.get(str(user_id), {}).get("subscription")
    if sub:
        return datetime.fromisoformat(sub)
    return None

def set_subscription(user_id, username, days, trial=False):
    data = load_data()
    exp = datetime.utcnow() + timedelta(days=days)
    data[str(user_id)] = {
        "subscription": exp.isoformat(),
        "username": username,
        "trial_used": trial,
        "v2ray_key": ""
    }
    save_data(data)
    return exp

def has_used_trial(user_id):
    data = load_data()
    return data.get(str(user_id), {}).get("trial_used", False)

def deactivate_expired_users():
    now = datetime.utcnow()
    data = load_data()
    for uid in list(data.keys()):
        exp = data[uid].get("subscription")
        if exp and datetime.fromisoformat(exp) < now:
            data[uid]["subscription"] = None
    save_data(data)

def get_all_users():
    data = load_data()
    return list(data.keys())

def is_admin(user_id):
    try:
        with open(ADMINS_FILE, "r") as f:
            admins = json.load(f)
        return str(user_id) in admins.get("admins", [])
    except:
        return False

def is_moderator(user_id):
    try:
        with open(ADMINS_FILE, "r") as f:
            admins = json.load(f)
        return str(user_id) in admins.get("moderators", [])
    except:
        return False

def add_admin(user_id):
    with open(ADMINS_FILE, "r") as f:
        admins = json.load(f)
    if "admins" not in admins:
        admins["admins"] = []
    admins["admins"].append(str(user_id))
    with open(ADMINS_FILE, "w") as f:
        json.dump(admins, f, indent=2)

def remove_admin(user_id):
    with open(ADMINS_FILE, "r") as f:
        admins = json.load(f)
    if "admins" in admins and str(user_id) in admins["admins"]:
        admins["admins"].remove(str(user_id))
    with open(ADMINS_FILE, "w") as f:
        json.dump(admins, f, indent=2)

def delete_user(user_id):
    data = load_data()
    if str(user_id) in data:
        del data[str(user_id)]
    save_data(data)

def update_v2ray_key(user_id, key):
    data = load_data()
    if str(user_id) in data:
        data[str(user_id)]["v2ray_key"] = key
    save_data(data)

def get_v2ray_key(user_id):
    data = load_data()
    return data.get(str(user_id), {}).get("v2ray_key", "")
