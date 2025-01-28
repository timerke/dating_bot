from configparser import ConfigParser


def get_token(config_file: str) -> str:
    """
    :param config_file: path to configuration file.
    :return: bot token.
    """

    config_parser = ConfigParser()
    config_parser.read(config_file)
    return config_parser.get("GENERAL", "TOKEN")
