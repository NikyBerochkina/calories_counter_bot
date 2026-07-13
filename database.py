import aiosqlite

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    daily_goal INTEGER
);

CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    calories INTEGER NOT NULL,
    description TEXT NOT NULL,
    logged_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def ensure_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, daily_goal) VALUES (?, NULL)",
            (user_id,),
        )
        await db.commit()


async def add_entry(user_id: int, calories: int, description: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO entries (user_id, calories, description) VALUES (?, ?, ?)",
            (user_id, calories, description),
        )
        await db.commit()


async def delete_last_entry(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id FROM entries WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        )
        row = await cursor.fetchone()
        if row is None:
            return False
        await db.execute("DELETE FROM entries WHERE id = ?", (row[0],))
        await db.commit()
        return True


async def get_today_entries(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT calories, description, logged_at FROM entries
            WHERE user_id = ? AND date(logged_at) = date('now')
            ORDER BY id
            """,
            (user_id,),
        )
        return await cursor.fetchall()


async def get_week_summary(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT date(logged_at) AS day, SUM(calories) AS total
            FROM entries
            WHERE user_id = ? AND logged_at >= datetime('now', '-6 days')
            GROUP BY day
            ORDER BY day
            """,
            (user_id,),
        )
        return await cursor.fetchall()


async def set_goal(user_id: int, goal: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (user_id, daily_goal) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET daily_goal = excluded.daily_goal",
            (user_id, goal),
        )
        await db.commit()


async def get_goal(user_id: int) -> int | None:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT daily_goal FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else None
