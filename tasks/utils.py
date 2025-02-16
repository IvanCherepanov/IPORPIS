import os
import re
from pathlib import Path


def get_project_root():
    print(Path(__file__).parent.parent)
    return Path(__file__).parent.parent


def get_env_path():
    return os.path.join(get_project_root(), ".env")


def get_path_from_root(custom_path: str):
    return os.path.join(get_project_root(), custom_path)


def validate_email(email) -> bool:
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    pattern = re.compile(regex)

    if not pattern.match(email):
        return False

    return True
