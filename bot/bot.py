import telebot
from . import utils as ut


class Bot:
    """
    Main bot class.
    """

    def __init__(self) -> None:
        token = ut.get_token("config.ini")
        print(token)
        self._bot: telebot.TeleBot = telebot.TeleBot(token)

    def run(self) -> None:
        self._bot.infinity_polling()
