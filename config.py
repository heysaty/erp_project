import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class Settings:
    EMAIL_TOKEN = os.getenv("EMAIL_PASSWORD")


settings = Settings()
