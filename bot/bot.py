import telebot
from . import utils as ut
from .database import create_database


class Bot:
    """
    Main bot class.
    """

    def __init__(self) -> None:
        token = ut.get_token("config.ini")
        self._bot: telebot.TeleBot = telebot.TeleBot(token)
        self._add_handlers()
        create_database()

    def _add_handlers(self) -> None:
        self._bot.add_message_handler({"function": self._start,
                                       "filters": {"commands": ["start"]}
                                       })

    def _start(self, message: telebot.types.Message) -> None:
        print(type(message))

    def run(self) -> None:
        self._bot.infinity_polling()
