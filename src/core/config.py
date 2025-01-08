import sys
from datetime import timedelta
from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic import BaseModel, PostgresDsn, SecretStr
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("settings",)


class DbSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    name: str = "postgres"
    username: str = "postgres"
    password: SecretStr = SecretStr("postgres")

    def get_url(
        self,
        scheme: Literal["postgres", "postgresql", "postgresql+asyncpg"] = "postgresql+asyncpg",
        db_name: str | None = None,
    ) -> SecretStr:
        dsn = PostgresDsn.build(
            scheme=scheme,
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password.get_secret_value(),
            path=db_name or self.name,
        )
        return SecretStr(str(dsn))


class GoogleSettings(BaseModel):
    client_id: str = "111111111111-zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz.apps.googleusercontent.com"
    client_secret: str = "AAAAAA-zzzzzzzzz-zzzzzzzzzzzzzzzzzz"


class JWTSettings(BaseModel):
    secret_key: str = "secret-key"
    algorithm: Literal["HS256", "HS512"] = "HS256"
    access_token_lifetime: timedelta = timedelta(minutes=30)


class Config(BaseSettings):
    root_dir: Path = Path(__file__).parent.parent.parent.resolve()
    logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    jwt: JWTSettings = JWTSettings()
    google: GoogleSettings = GoogleSettings()
    db: DbSettings = DbSettings()

    project_title: str = "Let's Schedule"
    project_description: str = "Let's Schedule is an open-source API designed for scheduling events"
    app_host: Url = Url("http://localhost:8000")

    sentry_dsn: SecretStr = SecretStr("")

    model_config = SettingsConfigDict(
        env_file=f"{root_dir}/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        env_nested_delimiter="__",
        extra="ignore",  # ignores extra keys from env file
    )


settings = Config()

# Logging Configuration
logger.remove(0)

_logtime = "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
_loglevel = "<red>[{level}]</red>"
_logpath = "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
_logmsg = "<green>{message}</green>"
logger.add(
    sys.stderr,
    format=f"{_logtime} | {_loglevel} | {_logpath}: {_logmsg}",
    colorize=True,
    level=settings.logging_level,
    backtrace=True,
    diagnose=True,
)
