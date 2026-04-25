import os
from dotenv import load_dotenv

load_dotenv()


def load_credentials() -> tuple[str, str]:
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    if not username:
        raise EnvironmentError("INSTAGRAM_USERNAME not set in .env")
    if not password:
        raise EnvironmentError("INSTAGRAM_PASSWORD not set in .env")
    return username, password
