from typing import Optional
import telebot
from . import database as db, utils as ut


class Bot:
    """
    Main bot class.
    """

    def __init__(self) -> None:
        token = ut.get_token("config.ini")
        self._bot: telebot.TeleBot = telebot.TeleBot(token)
        self._add_handlers()
        db.create_database()

    def _add_handlers(self) -> None:
        self._bot.register_message_handler(self._change_user_photo, content_types=["photo"])
        self._bot.register_message_handler(self._register_user, regexp="Зарегистрироваться")
        self._bot.register_message_handler(self._start, commands=["start"])
        self._bot.register_message_handler(self._show_profile, regexp="Профиль")
        self._bot.register_message_handler(self._show_profile_photo, regexp="Фото")

    def _ask_user_to_register(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.add(telebot.types.KeyboardButton("Зарегистрироваться"))
        return self._bot.send_message(message.chat.id, "Хотите зарегистрироваться?", reply_markup=markup)

    @staticmethod
    def _get_user_id(message: telebot.types.Message) -> int:
        """
        :param message: message from user.
        :return: user ID in Telegram.
        """

        return message.from_user.id

    def _change_user_photo(self, message: telebot.types.Message):
        if message.caption and message.caption.lower() == "мое фото":
            file_id = message.photo[-1].file_id
            file_info = self._bot.get_file(file_id)
            downloaded_file = self._bot.download_file(file_info.file_path)

            user_tg_id = self._get_user_id(message)
            if not db.get_photo(user_tg_id):
                db.save_user_photo(user_tg_id, downloaded_file)
            else:
                db.update_user_photo(user_tg_id, downloaded_file)
            return self._bot.send_message(message.chat.id, "Ваше фото сохранено.")

    def _register_user(self, message: telebot.types.Message):
        user_id = self._get_user_id(message)
        if db.check_if_user_registered(user_id):
            return self._show_main_menu(message, "Вы уже зарегистрированы.")

        db.register_user(user_id, message.from_user.username)
        return self._show_main_menu(message, "Вы зарегистрированы.")

    def _show_main_menu(self, message: telebot.types.Message, text: Optional[str] = None):
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.add(*[telebot.types.KeyboardButton("Анкеты"),
                     telebot.types.KeyboardButton("Профиль"),
                     telebot.types.KeyboardButton("Совпадения")])
        text = text or "Главное меню"
        return self._bot.send_message(message.chat.id, text, reply_markup=markup)

    def _show_profile(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.add(telebot.types.KeyboardButton("Имя"))
        markup.add(telebot.types.KeyboardButton("Фамилия"))
        markup.add(telebot.types.KeyboardButton("Возраст"))
        markup.add(telebot.types.KeyboardButton("Пол"))
        markup.add(telebot.types.KeyboardButton("Фото"))
        markup.add(telebot.types.KeyboardButton("Возраст партнера"))
        return self._bot.send_message(message.chat.id, "Профиль", reply_markup=markup)

    def _show_profile_photo(self, message: telebot.types.Message):
        photo = db.get_photo(self._get_user_id(message))
        common_text = "В сообщении напишите: Мое фото."
        if photo is None:
            return self._bot.send_message(message.chat.id,
                                          "У Вас нет фото. Чтобы добавить фото, пришлите его в сообщении.<br>"
                                          f"{common_text}")

        return self._bot.send_photo(message.chat.id, photo,
                                    "Ваше фото. Чтобы заменить его, пришлите новое фото в сообщении.<br>"
                                    f"{common_text}")

    def _start(self, message: telebot.types.Message):
        if not db.check_if_user_registered(message.from_user.id):
            return self._ask_user_to_register(message)

        return self._show_main_menu(message)

    def run(self) -> None:
        self._bot.infinity_polling()
