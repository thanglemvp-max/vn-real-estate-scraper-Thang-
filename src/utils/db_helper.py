import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "scraping_status.db")


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Created directory: {db_dir}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS scrape_log (
                id TEXT PRIMARY KEY,
                url TEXT,
                scraped_date TEXT,
                status TEXT
            )
        ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")


def load_seen_ids():
    if not os.path.exists(DB_PATH):
        return set()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM scrape_log WHERE status = 'success'")
        return {str(row[0]) for row in cursor.fetchall()}
    except sqlite3.Error as e:
        print(f"Error loading IDs: {e}")
        return set()
    finally:
        conn.close()


def is_success(post_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM scrape_log WHERE id = ?", (str(post_id),))
    result = cursor.fetchone()
    conn.close()
    return result is not None and result[0] == 'success'


def update_status(post_id, url, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO scrape_log (id, url, scraped_date, status)
            VALUES (?, ?, ?, ?)
        ''', (str(post_id), url, now, status))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating status for {post_id}: {e}")
    finally:
        conn.close()


def get_stats():
    if not os.path.exists(DB_PATH):
        return {"success": 0, "failed": 0}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM scrape_log GROUP BY status")
    stats = dict(cursor.fetchall())
    conn.close()
    return stats