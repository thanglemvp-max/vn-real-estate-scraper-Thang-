import os

# File to store IDs locally
ID_LOG_FILE = "scraped_ids.txt"

def load_seen_ids():
    """ Loads all previously scraped IDs from text file into a set """
    if not os.path.exists(ID_LOG_FILE):
        return set()

    with open(ID_LOG_FILE, "r", encoding="utf-8") as f:
        # Strip whitespace and exclude empty lines
        return {line.strip() for line in f if line.strip()}

# Initialize the global set for O(1) lookup
seen_ids = load_seen_ids()

def is_duplicate(post_id):
    """ Checks if the post_id already exists in the memory set """
    return str(post_id) in seen_ids


def mark_as_scraped(post_id):
    """ Updates the memory set and persists the ID to the text file """
    pid_str = str(post_id)
    if pid_str not in seen_ids:
        # Add to memory for current session
        seen_ids.add(pid_str)

        # Append to physical file for future sessions
        with open(ID_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{pid_str}\n")