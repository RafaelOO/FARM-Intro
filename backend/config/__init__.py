from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Recruting"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://rortegao:MSmCbhLCIotDEMVl9KIIDbGq2zHX08fA8FNjwzqQ@cluster0.yvnvd.mongodb.net/recruting?retryWrites=true&w=majority"
    DB_NAME: str = "recruting"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
