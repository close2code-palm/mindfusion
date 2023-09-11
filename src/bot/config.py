import configparser
from dataclasses import dataclass


@dataclass
class Postgres:
    user: str
    password: str
    host: str
    port: int
    db_name: str

    @property
    def dsn(self):
        return (f'postgres://{self.user}:{self.password}'
                f'@{self.host}:{self.port}/{self.db_name}')


@dataclass
class Telegram:
    token: str
    webapp: str


@dataclass
class Amplitude:
    api_token: str


@dataclass
class Config:
    postgres: Postgres
    telegram: Telegram
    amplitude: Amplitude


def read_db_conf(config_path: str) -> Postgres:
    conf = configparser.ConfigParser()
    conf.read(config_path)
    postgres = conf['postgres']
    return Postgres(postgres.get('USER'), postgres.get('PASSWORD'), postgres.get('HOST'),
                    postgres.getint('PORT'), postgres.get('DB'))


def read_config(config_path: str) -> Config:
    conf = configparser.ConfigParser()
    conf.read(config_path)

    tg = conf['telegram']
    amplitude = conf['amplitude']

    return Config(
        read_db_conf(config_path),
        Telegram(tg.get('TOKEN'), tg.get('WEBAPP')),
        Amplitude(amplitude.get('API_KEY'))
    )
