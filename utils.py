import configparser
from dataclasses import dataclass


@dataclass
class Credentials:
    USER: str
    PASSWORD: str


@dataclass
class Bot:
    DB_PATH: str
    TOKEN: str


@dataclass
class Config:
    CREDENTIALS: Credentials
    BOT: Bot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    credentials = config['credentials']
    bot = config['db']

    return Config(CREDENTIALS=Credentials(
        USER=credentials['USER'],
        PASSWORD=credentials['password']),
        BOT=Bot(DB_PATH=bot['DB_PATH'], TOKEN=bot['TOKEN']),)
