import json
import re
import os

# Make script use its own directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

LEVEL_PATTERN = re.compile(r"(level\d{4})")

def extract_level_key(key):
    match = LEVEL_PATTERN.match(key)
    return match.group(1) if match else None

def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def build_standard_map(standard_json):
    mapping = {}
    for key in standard_json:
        level = extract_level_key(key)
        if level:
            mapping[level] = key
    return mapping

def normalize_file(standard_map, standard_json, target_json):
    result = {}
    seen_levels = set()

    for key, value in target_json.items():
        level = extract_level_key(key)

        if not level:
            print(f"[WARN] Invalid key format: {key}")
            continue

        if level in standard_map:
            std_key = standard_map[level]
            result[std_key] = value
            seen_levels.add(level)
        else:
            print(f"[EXTRA] Not in standard: {key}")

    for level, std_key in standard_map.items():
        if level not in seen_levels:
            print(f"[MISSING] Using standard for: {std_key}")
            result[std_key] = standard_json[std_key]

    return result


STANDARD_FILE = "tips_fs.json"
TARGET_FILE = "tips_fs_old.json"
OUTPUT_FILE = "normalized.json"

standard_json = load_json(STANDARD_FILE)
target_json = load_json(TARGET_FILE)

standard_map = build_standard_map(standard_json)

normalized = normalize_file(standard_map, standard_json, target_json)

save_json(normalized, OUTPUT_FILE)

print("Done.")