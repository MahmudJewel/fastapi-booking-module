from pydantic_settings import BaseSettings
from enum import Enum 

SECRET_KEY = "c00916a936dd2ae471eb32272ed7e749bb863b7e31f4f02f0bd4876463e1dc1b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"

class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True

class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    RELEASE_VERSION: str = "0.1"
    SHOW_SQL_ALCHEMY_QUERIES: int = 0
    SECRET_KEY: str = SECRET_KEY
    ALGORITHM: str = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = ACCESS_TOKEN_EXPIRE_MINUTES

config: Config = Config()
