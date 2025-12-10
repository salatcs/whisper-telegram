from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    BOT_TOKEN: str
    LOGGING_MODE: str = "all"
    DEFAULT_LOCALE: str = "ru"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "whisper"
    DB_USER: str = "postgres"
    DB_PASSWORD: str
    
    MIN_POOL_SIZE: int = 5
    MAX_POOL_SIZE: int = 50
    
    MAX_TTLCACHE_SIZE: int = 10_000

settings = Settings()