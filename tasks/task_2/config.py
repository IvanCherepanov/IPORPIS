import logging
from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from tasks.utils import get_env_path


class AppSettings(BaseSettings):
    yandex_smpt_login: str
    yandex_smpt_password: str

    log_file: Optional[str] = 'app.log'
    log_level: Optional[int] = logging.INFO

    class Config:
        extra='ignore'
        env_file = get_env_path()
        env_file_encoding = 'utf-8'


config = AppSettings()
