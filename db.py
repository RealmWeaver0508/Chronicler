import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def ensure_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_id, xp, level) VALUES (%s, 0, 0) ON CONFLICT (user_id) DO NOTHING", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def add_xp(user_id, amount):
    ensure_user(user_id)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET xp = xp + %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    cur.close()
    conn.close()

def get_user_xp(user_id):
    ensure_user(user_id)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT xp FROM users WHERE user_id = %s", (user_id,))
    xp = cur.fetchone()[0]
    conn.close()
    return xp

def get_user_level(user_id):
    ensure_user(user_id)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT level FROM users WHERE user_id = %s", (user_id,))
    level = cur.fetchone()[0]
    conn.close()
    return level

def set_user_level(user_id, new_level):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET level = %s WHERE user_id = %s", (new_level, user_id))
    conn.commit()
    cur.close()
    conn.close()

def get_leaderboard(limit=10):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, xp, level FROM users ORDER BY level DESC, xp DESC LIMIT %s", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
