from bot import Bot, set_logger


def run() -> None:
    set_logger()
    dating_bot = Bot()
    dating_bot.run()


if __name__ == "__main__":
    run()
