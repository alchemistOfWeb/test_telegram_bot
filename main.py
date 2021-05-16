import config
from bot import Bot


if __name__ == '__main__':
    bot_ = Bot(bot_token=config.BOT_TOKEN)
    bot_.run()
