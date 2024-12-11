from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_WEBHOOK_URL: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USER: str
    RABBIT_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file='./config/.env')

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASSWORD}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"

settings = Settings()
