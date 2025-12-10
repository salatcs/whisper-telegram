from asyncpg import connect

from ..config import settings

async def init_db():
    conn = await connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
    )
    
    try:
        await conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            tg_id BIGINT NOT NULL UNIQUE,
            username VARCHAR(32),
            name TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            in_bot BOOLEAN DEFAULT FALSE
        )""")
        await conn.execute("""CREATE TABLE IF NOT EXISTS whispers (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            inline_message_id TEXT,
            from_id BIGINT NOT NULL,
            to_id BIGINT,
            to_username VARCHAR(32),
            text VARCHAR(200)
        )""")
    finally:
        await conn.close()