import sys
from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic import BaseModel, PostgresDsn, SecretStr
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
    ) -> SecretStr:
        dsn = PostgresDsn.build(
            scheme=scheme,
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password.get_secret_value(),
            path=self.name,
        )
        return SecretStr(str(dsn))


class Config(BaseSettings):
    root_dir: Path = Path(__file__).parent.parent.parent.resolve()
    logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    db: DbSettings = DbSettings()

    project_title: str = "Let's Schedule"
    project_description: str = "Let's Schedule is an open-source API designed for scheduling events"

    sentry_dsn: SecretStr = SecretStr("")

    model_config = SettingsConfigDict(
        env_file=f"{root_dir}/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        env_nested_delimiter="_",
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
