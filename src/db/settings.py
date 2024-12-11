from pydantic_settings import BaseSettings, SettingsConfigDict

class AlembicSettings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DEBUG: bool

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST if (not self.DEBUG) else 'localhost'}:{self.DB_PORT}/{self.DB_NAME}"

settings = AlembicSettings()