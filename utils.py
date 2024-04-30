import configparser
from dataclasses import dataclass


@dataclass
class Bot:
    DB_PATH: str
    TOKEN: str


@dataclass
class Config:
    BOT: Bot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    bot = config['bot']

    return Config(BOT=Bot(DB_PATH=bot['DB_PATH'], TOKEN=bot['TOKEN']))
