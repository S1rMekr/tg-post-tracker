from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    rapid_api_key: str


@dataclass
class Config:
    tg_bot: TgBot


@dataclass
class RapidAPI:
    rapid_api_key: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            rapid_api_key=env('RAPID_API_KEY')
        )
    )
