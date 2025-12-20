import yaml
import re
import os

POST_ID_PATTERN = re.compile(r"pr(\d+)$")
ID_LOG_FILE = "scraped_ids.txt"

def generate_id(url):
    """
    Extract the unique post identifier from listing URL.
    """
    match = POST_ID_PATTERN.search(url)
    return match.group(1) if match else None


def load_seen_ids():
    """
    Loads all previously scraped IDs from text file into a set.
    """
    if not os.path.exists(ID_LOG_FILE):
        return set()

    with open(ID_LOG_FILE, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}

# Initialize the global set for O(1) lookup
seen_ids = load_seen_ids()

def is_duplicate(post_id):
    """
    Checks if the post_id already exists in the memory set.
    """
    return str(post_id) in seen_ids


def mark_as_scraped(post_id):
    """
    Updates the memory set and persists the ID to the text file.
    """
    pid_str = str(post_id)
    if pid_str not in seen_ids:
        # Add to memory for current session
        seen_ids.add(pid_str)

        with open(ID_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{pid_str}\n")


def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Not found config: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config