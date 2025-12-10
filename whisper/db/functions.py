from typing import Optional

from asyncpg.connection import Connection

async def check_name(tg_id: Optional[int], username: Optional[str], session: Connection):
    value = await session.fetchval("SELECT name FROM users WHERE tg_id = $1 OR username = $2", tg_id, username)
    return value or ("@" + username if username else None) or tg_id
    
async def create_whisper(from_id: int, to_id: Optional[int], to_username: Optional[str], text: str, inline_message_id: str, session: Connection):
    await session.execute("INSERT INTO whispers (from_id, to_id, to_username, text, inline_message_id) " \
                          "VALUES ($1, $2, $3, $4, $5)", from_id, to_id, to_username, text, inline_message_id)
    
async def find_whisper(inline_message_id: str, session: Connection):
    return await session.fetchrow("SELECT * FROM whispers WHERE inline_message_id = $1", inline_message_id)

async def init_db_user(tg_id: int, username: Optional[str], name: str, session: Connection):
    await session.execute("INSERT INTO users (tg_id, username, name) VALUES ($1, $2, $3) " \
                          "ON CONFLICT (tg_id) DO UPDATE SET username = EXCLUDED.username, name = EXCLUDED.name",
                          tg_id, username, name)

async def get_most_users(for_user: int, session: Connection):
    return await session.fetch("SELECT u.* FROM users u " \
        "JOIN whispers w ON u.tg_id = w.to_id OR u.username = w.to_username " \
        "WHERE w.from_id = $1 " \
        "GROUP BY u.id ORDER BY COUNT(w.id) DESC LIMIT 5", for_user)

async def add_in_bot(tg_id: int, session: Connection):
    await session.execute("UPDATE users SET in_bot = true WHERE tg_id = $1", tg_id)