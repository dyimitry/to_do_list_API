from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    host: str

    class Config:
        env_file = '.env'


settings = Settings()
