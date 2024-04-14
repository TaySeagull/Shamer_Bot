import configparser


def load_config(path: str):
    parser = configparser.ConfigParser()
    parser.read(path)

    settings = parser['SETTINGS']
    return settings
