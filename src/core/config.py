from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str

    SECRET_KEY: str
    DEVELOP_KEY: str
    ALGORITHM: str

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    USER_DB: str
    MODEL_DB: str
    TRANSACTION_DB: str
    PREDICTIONS_DB: str

    class Config:
        case_sensitive = True
        env_file = ".env"


config = Configs()
